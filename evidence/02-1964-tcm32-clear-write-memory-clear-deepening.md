# Case 02 deepening — TCM-32 clear/write and whole-stack memory-clear semantics, 1964

This evidence addendum deepens [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) without reopening the general history of magnetic-core memory.

**Bounded question:** once classic core memory is already known to retain state through remanence and to use destructive read/restore in an important historical regime, what did a later production core-memory manual mean by `Clear/Write` and `Memory Clear`? In particular, does `clear` name a separate Flash-like erase process, a selected-word overwrite step, or a broader electrical reset operation?

The answer matters for the repository's forgetting vocabulary. A nonvolatile state can survive loss of ordinary holding power yet still be deliberately reset by a powered operation; moreover, the historical word `clear` can refer to more than one **scope** of state change inside one product family.

---

## Source A — Computer Control Company TCM-32 manual, May 1964

**Document:** Computer Control Company, Inc. (3C), *Instruction Manual: Magnetic Core Memory Systems, Series TCM-32*, Document No. 71-218, May 1964.

**Preserved scan:** <https://bitsavers.org/pdf/computerControlCompany/71-218_3C_TCM-32_Core_Memory_Maint_May64.pdf>

**Evidence class:** `H/P` — manufacturer operating and maintenance manual for a named production core-memory system. Bitsavers is the preservation host, not the historical author.

This 1964 manual is deliberately used as a **later implementation/terminology witness**. It does not change Case 02's 1950–1954 MIT/Whirlwind anchor and is not evidence that Whirlwind used the same optional bulk-clear circuit.

---

## A1. Static retention does not require holding power

In §3-1.5, **Information Retention**, the manual states that the magnetic-core unit does not require power for its static memory capability: power is needed to switch cores between states, not to hold them there. It attributes the retained state to the retentivity of the magnetic material and says that, absent a severe transient, the core stack retains stored information after power removal.

The manual uses the word `indefinitely`. That wording is useful as a period product claim, but this addendum does **not** turn it into a measured universal retention duration for every ferrite core, array, environment, or machine.

**Historical boundary:** `power-off retention != immunity to a later switching/reset pulse`.

---

## A2. Ordinary writing assumes a selected address has first been cleared to ZERO

In §3-1.4, **Writing**, the manual says that before write half-currents are applied, all cores at the **selected address** have been cleared to the `ZERO` state. The write currents tend to switch the selected word's cores to `ONE`; inhibit currents prevent selected bit planes that should remain zero from making that transition.

This is not a separate block-erase geometry comparable to Flash. It is a state-setting phase inside the magnetic-memory write protocol:

```text
selected address
    -> force selected cores to ZERO reference state
    -> apply write currents
    -> inhibit bit planes that must stay ZERO
    -> new word remains in the selected address
```

**Historical record:** a production core-memory manual can use `clear` for the reference-state step that precedes writing a new selected word.

---

## A3. `Clear/Write` and `Read/Regenerate` have different continuation semantics

The manual's operating-cycle description makes the distinction explicit.

For **Clear/Write**, the selected storage location is first cleared of prior information and then the new information-register word is written into that location. The old stored word is not first transferred into the information register for preservation.

For **Read/Regenerate**, the existing word is read into the information register and then identical information is restored to the selected memory location.

The two operations can therefore share a core-switching substrate while having opposite relations to the old logical value:

```text
Clear/Write:
old word -> intentionally discarded at the selected address -> new word written

Read/Regenerate:
old word -> sensed/copied -> old word restored
```

**Grounded boundary:** `clear/write != destructive read followed by regeneration`, even though both can pass through a ZERO reference state.

---

## A4. The same system also exposes a whole-stack `Memory Clear` option

The manual separately lists **Memory Clear** as an option and describes it as clearing all information contained in the core stack with one operation.

The dedicated **Memory Clear Driver PAC, model S-103** section is even more explicit. The driver supplies clear current to the memory inhibit windings, and the manual states that this current **resets all cores to the ZERO state**.

This gives a scope contrast inside one named system:

```text
selected-address Clear/Write
    !=
whole-stack Memory Clear
```

Both are electrical state-setting operations. The latter is not described as demagnetizing the material into a neutral/non-state condition; it resets the array to the system's defined `ZERO` state.

**Grounded boundary:** `bulk memory clear != physical demagnetization`.

---

## A5. Bulk clear has its own operational recovery constraints

The S-103 section says a memory-clear pulse must not be applied during a normal memory cycle. After a clear pulse, no other system pulses should be applied for **200 microseconds** so the power supply can recover; the manual also limits the number of clear pulses in a 10-millisecond interval.

The exact numbers are product-specific. Their methodological value is more general but still bounded:

> an operation that forgets retained payload can itself impose a temporary power/service recovery obligation.

So `clear completed` and `memory ready for ordinary next-cycle service` need not be the same instant.

---

## Engineering reconstruction

### E1. Quiescent nonvolatility != reset immunity

The TCM-32 can make both claims in the same manual:

- the cores need no holding power for static retention;
- powered clear/write or Memory Clear currents can intentionally switch that retained state.

Therefore `nonvolatile` means neither `immutable` nor `cannot be deliberately forgotten electrically`.

### E2. `Clear` is typed by scope

One historical vocabulary item is insufficient without an operation scope:

```text
clear selected address
clear information register
clear address register
Memory Clear whole core stack
```

The repository should therefore ask **what state population is authorized to change** whenever a source uses `clear`, rather than importing one modern deletion/erase meaning.

### E3. Magnetic-core overwrite != Flash erase-before-write

There is a useful functional comparison and an important stop condition.

Both mechanisms can include a state-reset phase before a desired new value is established. But classic core switching is a reversible transition between remanent magnetic states at the selected word/bit population, whereas Flash erase changes floating-gate/charge state over an erase geometry and carries different programming asymmetry, endurance, and controller consequences.

Safe analogy: `rewrite may require a reference-state transition`.

Rejected identity: `TCM-32 Clear/Write = Flash erase-before-write`.

### E4. Bulk clear != evidence that the previous word remains as a separately addressable stale embodiment

Mapped Flash can leave obsolete physical pages after a logical update. The bounded TCM-32 clear evidence does not establish an equivalent shadow/stale copy. Once the selected cores have been switched to the reference state, ordinary core addressing does not reveal a second preserved embodiment of the prior word merely because the logical write was staged as clear-then-write.

This does not make claims about analog forensic remanence after magnetic switching; no such measurement is present in the manual.

---

## Historical / anti-overclaim boundaries

- The TCM-32 manual is a **1964 implementation witness**, not an invention-priority record for `clear`, `overwrite`, core reset, or bulk memory clearing.
- Its whole-stack Memory Clear option must not be projected backward onto the exact MIT Memory Test Computer / Whirlwind circuitry without separate evidence.
- `Clear/Write` is not a claim that every magnetic-core memory used the identical sequencing, word organization, current levels, or option set.
- The manual's `indefinitely` retention language is a manufacturer operational claim under a stated no-severe-transient condition, not a universal measured lifetime.
- Electrical reset to the ZERO state is not evidence of secure sanitization against every possible lower-level/analog recovery technique.

---

## Related-repository boundary

The broad historical mechanism, coincident-current selection, manufacturing labor, and system-level reasons core memory was attractive are already covered in [`tmzncty/computing-archaeology: Why Was Magnetic-Core Memory Worth Weaving by Hand?`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md).

This addendum keeps only the retention-specific distinction:

> **a quiescently nonvolatile core state can be deliberately replaced through a selected-address clear/write sequence or reset across the whole stack by a separate memory-clear operation; `clear` therefore needs both mechanism and scope before it can be compared with `overwrite`, `erase`, or `forgetting`.**

---

## Readiness assessment

This slice substantially improves Case 02's **write / clear / reset** semantics and partially advances the roadmap's magnetic overwrite / physical-reset vocabulary. It does **not** close magnetic-disk/tape overwrite, degaussing, analog remanence after switching, secure sanitization, or the broader genealogy of memory-clear operations.
