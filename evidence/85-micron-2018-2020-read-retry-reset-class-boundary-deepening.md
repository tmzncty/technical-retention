# Case 85 Deepening — Micron 2018–2020 Read-Retry Reset-Class Boundary

**Case:** [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md)  
**Status:** `bounded deepening complete`  
**Question:** does a NAND `RESET` operation necessarily retire the currently selected read-retry state, or do different reset classes define different persistence horizons for reader configuration?

---

## 1. Why this slice exists

The existing Micron deepening for Case 85 established a deliberately narrow contract for the L83A 32Gb MLC family in 2015:

```text
SET FEATURES 89h = retry option N
    -> following reads use option N
    -> option N remains selected until 89h is rewritten
       or the device is powered down
```

That source gave a direct **power boundary**, but it did not independently establish what an ordinary `RESET (FFh)`, `SYNCHRONOUS RESET (FCh)`, or `RESET LUN (FAh)` did to feature address `89h`. The earlier evidence therefore left reset as a separate source question rather than silently equating `reset` with `power-down`.

This slice follows that debt with a later Micron-primary patent family whose priority is **2018-01-12** and which explicitly discusses:

- feature address `89h`;
- ordinary reset commands including `FFh`, `FCh`, and `FAh`;
- a distinct `Hard Reset (FDh)`;
- custom read-retry scratch state;
- internal SRAM;
- power-cycle behavior.

The result is not a retroactive answer for every 2015 L83A device. It is a later Micron-primary witness that **reset is not one undifferentiated state-retirement event** in read-retry designs.

The bounded contribution is therefore:

```text
power-down boundary
    !=
generic reset boundary

ordinary reset class
    !=
hard-reset class

"put target into a known condition"
    !=
"every mutable feature returns to default"
```

---

## 2. Source ledger

### Source A — Micron L83A 32Gb MLC NAND datasheet, Rev. A, May 2015

Micron Technology, **“32Gb, Asynchronous/Synchronous NAND”**, `L83A_32Gb_Async_Sync_NAND_mlc_plus.pdf`, Rev. A 5/15 EN, PDF ID `09005aef8644c380`.

Public mirrors inspected for this project:

- <https://www.unikeyic.com/media/datasheet/d9/6b/ded2/d9/8c2c3bd5996175045d2af62c6e827efe.pdf>
- <https://atta.szlcsc.com/upload/public/pdf/source/20190812/C410864_03C665DBBF4D218514A1FCC9D716C19A.pdf>

Relevant printed sections/pages:

- `RESET (FFh)`, printed p. 42;
- `SYNCHRONOUS RESET (FCh)`, printed p. 43;
- configuration-feature reset notes around printed pp. 64–67;
- `Read Retry Operations`, printed pp. 87–88.

Source A is used for the exact L83A bounded claims already present in Case 85:

- feature address `89h` selects read-retry state;
- following reads use that state;
- the read-retry section explicitly ends the selected-state lifetime when `89h` is rewritten or the device is powered down;
- the reset section documents some state retirement but does not, in the inspected clauses, state that `FFh` resets feature `89h`.

### Source B — Micron `Read retry scratch space` patent family

Micron Technology, **“Read retry scratch space”**, represented here by:

- US20200371876A1, published **2020-11-26**;
- US11586498B2, granted **2023-02-21**;
- priority **2018-01-12**;
- inventors Rahul Mitchell Jairaj, Mark A. Hawes, and Terry M. Grunzke;
- assignee Micron Technology, Inc.

Google Patents record inspected:

- <https://patents.google.com/patent/US11586498B2/en>

This source is a patent disclosure, not a shipping-product conformance report. It is used as a **Micron-primary design witness** for the reset-class distinction and read-retry scratch-state lifetime.

### Companion-repository check

`tmzncty/computing-archaeology` was searched again for `read retry 89h reset`. No dedicated reusable packet was found.

Broad Micron NAND command genealogy, `FFh/FCh/FAh/FDh` standardization history, device-family adoption, controller firmware history, and cross-vendor reset semantics remain appropriate for `computing-archaeology`. This record keeps only the retention-specific state-lifetime seam.

---

## 3. Historical record — the 2015 L83A source proves a power boundary, not a universal reset boundary

### 3.1 Selected read-retry state survives multiple reads

Micron's 2015 L83A datasheet says that after the host writes the read-retry feature address, subsequent reads use the associated internal NAND settings until either:

1. the feature address is rewritten; or
2. the device is powered down.

That establishes command-to-command persistence for the selected reader configuration.

It does **not** by itself establish what every reset command does to `89h`.

### 3.2 `RESET (FFh)` retires some state, but not all feature state by definition

The same L83A document describes `RESET (FFh)` as putting a target into a known condition and aborting command sequences in progress. It clears or invalidates command/data/cache state, cancels pending operations, and can alter interface/timing state.

But the document also demonstrates that reset effects are **feature-specific**. For example, the timing-mode/data-interface behavior depends on whether the synchronous or asynchronous interface is active, and another configuration note explicitly states reset-to-default behavior for a particular array-operation-mode field.

This matters because the safe historical inference is only:

```text
FFh retires documented classes of runtime state
```

not:

```text
FFh necessarily restores every feature address to default
```

For L83A feature `89h` specifically, the inspected read-retry text says `rewrite or power-down`; it does not supply a direct `FFh -> 89h default` clause.

### 3.3 therefore the earlier Case 85 non-claim was correct

The 2015 source supports:

```text
mode persists across reads
    !=
mode persists across power
```

It does not support, without another source:

```text
any RESET command
    =
power-down for feature 89h
```

This slice keeps that exact-family caution intact.

---

## 4. Historical record — the later Micron family explicitly distinguishes ordinary reset from Hard Reset

### 4.1 ordinary reset commands may leave feature 89h selected

The 2018-priority Micron patent family states, in an example, that reset commands such as:

- `FFh`;
- `FCh`;
- `FAh`;

**may not reset** Read Retry feature address `89h` P1 data and disable Read Retry.

The wording matters. The source does not say that every implementation must preserve `89h` across all three commands. It says these reset commands **may not** do the state-retirement job assumed by a simplistic `reset clears retry state` model.

This is enough to reject the universal equivalence:

```text
reset command
    -> read-retry state necessarily defaulted
```

### 4.2 Hard Reset is a distinct retirement authority

The same Micron disclosure immediately states that a **Hard Reset (`FDh`)** command can reset Read Retry feature address `89h` to its default value for a target LUN.

Thus the historical/design record itself exposes at least two reset classes:

```text
FFh / FCh / FAh
    ordinary reset examples
    may not retire feature-89h state

FDh
    hard-reset example
    can restore feature 89h to default
```

The important retention fact is not merely that `FDh` exists. It is that **the command class participates in defining the persistence horizon of reader-control state**.

### 4.3 `known condition` therefore cannot be treated as `all state forgotten`

A broad phrase such as `put the device into a known condition` is insufficient to infer complete feature-state retirement.

The later Micron disclosure supplies a direct counterexample shape:

```text
reset event occurred
    +
selected retry state may remain
```

while another reset class can explicitly retire that state.

The interpreter must therefore ask which reset command, which feature, which target scope, and which device/design regime are involved.

---

## 5. Historical record — custom retry state introduces another transient embodiment

### 5.1 scratch-space retry can retain a learned/useful reader condition for future reads

The Micron patent proposes `Read Retry Scratch Space` so a host/controller can load custom or previously successful read-retry offsets and invoke them again on later reads. A successful retry can therefore become a reusable reader hint without rewriting the user payload.

This extends the Case 85 distinction:

```text
payload physical state
    !=
reader configuration used to recover it
```

with a further layer:

```text
preset retry state space
    !=
custom scratch retry state
```

### 5.2 custom retry scratch state can live in internal SRAM

In one disclosed example, custom Read Retry scratch space is loaded into **internal SRAM**.

That is a useful embodiment boundary because it prevents the word `stored` from being read automatically as `nonvolatile`.

The source itself then states that custom Read Retry can be reset using:

- `Hard Reset (FDh)`; or
- a power cycle.

The disclosed scratch state is therefore reusable across later reads while still having a deliberately bounded reset/power lifetime.

### 5.3 learned recovery advice can be useful without becoming archival state

The disclosure's future-read reuse pattern supports:

```text
successful retry result
    -> reusable reader hint
    -> later read attempt can start from that hint
```

but not:

```text
successful retry result
    -> permanent per-page recovery history
```

The same architecture can deliberately keep the hint in volatile internal SRAM.

---

## 6. Engineering reconstruction — reset is a vector of state-retirement effects

Project reconstruction:

> A reset should not be modeled as one scalar fact `reset happened`. For retention analysis it is a **vector of state-retirement effects** whose components can differ by command, feature, target scope, interface state, and device generation.

For this bounded material, at least the following questions are distinct:

1. were command sequences aborted?
2. were data/cache registers invalidated?
3. was interface/timing state changed?
4. was feature `89h` returned to default?
5. was custom read-retry SRAM cleared?
6. was user NAND payload modified?
7. did the whole device lose power?

A single word `reset` cannot answer all seven.

This gives the bounded chain:

```text
RESET command accepted
    !=
all runtime state retired
    !=
feature 89h defaulted
    !=
custom scratch state cleared
    !=
power removed
    !=
user payload erased
```

---

## 7. Engineering reconstruction — state lifetime must be attached to a specific event class

The combined evidence now supports several different horizons for read-retry state:

```text
across one READ
    <
across multiple READ commands
    <
possibly across some ordinary reset commands
    <
until a feature-specific Hard Reset or power cycle
```

The exact ordering is **not universal**; the point is that these are separate source questions.

For a named implementation, a persistence statement should therefore take the form:

```text
state S survives event class E
```

rather than:

```text
state S is persistent
```

This is an engineering-reconstruction rule derived from the source distinctions, not Micron's historical vocabulary.

---

## 8. Engineering reconstruction — power-retained payload can coexist with reset-bounded interpretation state

The NAND payload and the reader-control state can have different event horizons.

A bounded example is:

```text
nonvolatile NAND threshold state
    survives ordinary power-off by design

while

active/custom read-retry state
    can be retired by FDh or power cycle
```

After the reader-control state disappears, the payload has not thereby been erased. The system may be able to rediscover capability, rerun retry search, and re-establish a useful interpretation state.

Therefore:

```text
reader-state loss
    !=
payload loss
```

and:

```text
functional continuity after restart
    does not require
bitwise continuity of the previous reader configuration
```

provided the required read relation can be reconstructed.

---

## 9. Engineering reconstruction — stronger reset can be an authority boundary rather than a physical repair

`FDh` in the later Micron example changes the authority/currentness of read-retry configuration. It does not repair cell wear, restore threshold distributions, refresh data, or rewrite the page.

Thus:

```text
hard-reset completion
    !=
media refresh completion
```

The hard reset can retire one interpretation state while leaving the underlying physical representation untouched.

This separation matters for Case 85 because a default read after state retirement can again fail even though a previous custom retry setting had successfully recovered the same payload.

---

## 10. Functional comparison — not genealogy

### 10.1 Case 38 — Intel S3700 Feature Control

Case 38 distinguishes current feature state from saved/nonvolatile feature state and keeps reset/power-cycle behavior feature-specific.

Case 85 now provides a NAND-side counterpart:

```text
feature supported
    !=
feature currently selected
    !=
feature survives ordinary reset
    !=
feature survives hard reset/power
```

This is a functional comparison of persistence horizons, not evidence of shared implementation or historical descent.

### 10.2 Case 149 — Micron OTP mode versus irreversible OTP authority

Case 149 distinguishes volatile mode selection from a separately persistent or irreversible protection relation.

Case 85 adds another Micron-family example in which short-lived command/control state and durable media state coexist:

```text
volatile / reset-bounded access or interpretation mode
    !=
nonvolatile substrate state
```

Again, this is not a claim that OTP mode and Read Retry use the same registers, circuitry, or firmware.

### 10.3 Case 36 — refresh remains separate

Case 36 concerns representation renewal by correcting and rewriting data. Case 85's reset-class distinction affects how the current physical state is interpreted.

Therefore:

```text
reset reader state
    !=
refresh payload state
```

---

## 11. Functional analogy — explicitly nonhistorical

A bounded analogy is a receiver with a tuning preset and more than one reset button:

- one reset aborts the current transaction but leaves the selected tuning preset intact;
- a stronger reset restores the tuning preset to its default;
- removing power also clears the preset;
- the signal source itself remains physically present.

This analogy illustrates **event-specific control-state lifetime** only. It provides no evidence about NAND implementation, command genealogy, or voltage behavior.

---

## 12. Philosophical interpretation — bounded

The narrow interpretive point is:

> `restart` or `reset` is not a metaphysical return to an original state; it is a technically specified retirement of some relations and preservation of others.

For this case, the relevant question is not simply whether `the device was reset`, but which interpretation state lost authority and which substrate state remained.

This does not imply that technical state is purely semantic. The physical NAND state, volatile SRAM state, command decoder, feature registers, and power domains materially constrain what can survive each event.

The useful proposition is only:

> continuity and discontinuity are **state-class × event-class relations**, not properties of a device taken as an undifferentiated whole.

---

## 13. Explicit non-claims

This slice does **not** claim that:

1. Micron invented read retry.
2. Micron invented Hard Reset.
3. the 2018-priority patent is the first NAND design to distinguish reset classes.
4. the patent proves every disclosed embodiment shipped in a commercial product.
5. every Micron NAND implements `FDh`.
6. every Micron NAND preserves feature `89h` across `FFh`, `FCh`, or `FAh`.
7. every `FFh`, `FCh`, or `FAh` necessarily preserves `89h`; the patent says these commands **may not** reset it in an example.
8. the 2015 L83A family is proven to preserve feature `89h` across `FFh`.
9. the 2015 L83A family is proven to clear feature `89h` on `FFh`.
10. the later patent's reset semantics can be projected backward onto the exact 2015 L83A silicon.
11. `power-down`, `FFh`, `FCh`, `FAh`, and `FDh` are equivalent events.
12. putting a target into a `known condition` means every feature register is at its default value.
13. custom read-retry scratch state is necessarily nonvolatile because it is called `stored` or `scratch space`.
14. internal SRAM is the only possible embodiment of read-retry scratch state in every implementation.
15. clearing read-retry state erases user data.
16. clearing read-retry state refreshes or repairs NAND cells.
17. a successful custom retry setting remains optimal indefinitely.
18. a successful retry setting is necessarily stored per page, per block, or across power by an SSD controller.
19. a patent disclosure proves controller firmware conformance in any named SSD.
20. later Micron reset-class behavior establishes cross-vendor NAND reset semantics.
21. the command codes discussed here are universally standardized with identical semantics across all NAND generations.
22. the source establishes the full genealogy of `FDh`, ARC, Corrective Read, custom retry scratch space, or read-offset registers.

---

## 14. Claim ledger

| Claim | Class | Evidence strength | Boundary |
|---|---|---:|---|
| Micron L83A 2015 says selected read-retry state lasts until feature rewrite or power-down | historical/vendor record | strong | exact L83A family, Rev. A 5/15 |
| L83A `RESET (FFh)` aborts operations and retires documented command/cache/interface state | historical/vendor record | strong | exact reset clauses |
| L83A reset effects are feature/interface specific | historical/vendor record | strong | timing/data-interface and array-operation-mode notes |
| inspected L83A read-retry text does not itself establish `FFh -> 89h default` | source-boundary statement | strong | absence is limited to inspected clauses; not proof of opposite behavior |
| 2018-priority Micron family states `FFh/FCh/FAh` may not reset 89h in an example | historical/design record | strong | patent embodiment wording, not universal product contract |
| the same family states `FDh` can reset 89h to default for a target LUN | historical/design record | strong | patent embodiment wording |
| custom retry state can be loaded into internal SRAM | historical/design record | strong | disclosed example |
| custom retry can be reset by FDh or power cycle | historical/design record | strong | disclosed example |
| generic `reset` is too coarse to specify reader-state lifetime | engineering reconstruction | strong | supported by differentiated reset commands/effects |
| event-specific state lifetime is a better model than a scalar `persistent/transient` label | engineering reconstruction | strong | bounded to analyzed evidence |
| later Micron evidence proves exact 2015 L83A 89h-on-FFh behavior | rejected claim | unsupported | remains open |

---

## 15. Prior-art / chronology boundary

Safe chronology:

- by **May 2015**, Micron's L83A family publicly documented a selected read-retry state lasting across reads until feature rewrite or power-down;
- with priority **2018-01-12**, Micron's later Read Retry Scratch Space family explicitly distinguished ordinary reset examples (`FFh/FCh/FAh`) from `Hard Reset (FDh)` for feature-`89h` retirement;
- the U.S. application was published as US20200371876A1 on **2020-11-26**.

Unsafe chronology:

- `FDh` was invented in 2018;
- 2018 is the first time any NAND reset class differed from another;
- the patent establishes the first commercial deployment of these semantics;
- the later patent proves the exact 2015 L83A reset behavior.

The historical value of this slice is a **floor for a directly documented Micron reset-class distinction**, not an invention-priority claim.

---

## 16. Remaining evidence debt

This slice **partially closes and reframes** the earlier reset-semantic debt.

Now directly established:

- Micron had a later design regime in which ordinary reset commands and Hard Reset could differ with respect to read-retry state;
- custom retry scratch state could be kept in internal SRAM and explicitly cleared by FDh or power cycle;
- therefore `reset` must be named precisely before assigning a read-retry persistence horizon.

Still open:

- exact feature-`89h` behavior across `RESET (FFh)`, `SYNCHRONOUS RESET (FCh)`, and `RESET LUN (FAh)` for the **2015 L83A** family itself;
- recovery of the pre-2014/2014-era revision of the exact `MT29F32G08CBADA` datasheet used around the Linux Micron read-retry merge;
- a shipping-product/family datasheet that directly states the `FDh -> 89h default` relation, independently of the patent disclosure;
- Hynix-primary documentation for the 1x-nm MLC retry-OTP/calibration regime already seen through Linux;
- broader `FFh/FCh/FAh/FDh` NAND command genealogy and cross-vendor adoption, which belongs in `computing-archaeology`.

---

## 17. Completion decision

This is a **bounded deepening**, not a new case and not a maturity promotion.

It adds one precise retention boundary to Case 85:

```text
selected reader state survives some operations
    !=
selected reader state survives every reset class

ordinary reset
    !=
hard reset
    !=
power cycle

payload retention
    !=
reader-configuration retention
```

Case 85 should remain **`grounded`**.

The strongest new caution is also the simplest:

> **Never write `reset clears the read-retry state` unless the source names both the reset event and the feature whose state is being retired.**
