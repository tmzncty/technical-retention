# Evidence 85E — Micron L83A 2015 read-retry reset survival: RESET aborts work without necessarily retiring feature `89h`

## Status

**`bounded deepening complete`** — this packet closes one source-reading debt left by the earlier Micron L83A evidence: the exact-family relationship between read-retry feature address `89h` and the documented `RESET (FFh)`, `SYNCHRONOUS RESET (FCh)`, and `RESET LUN (FAh)` commands.

This is also a **correction addendum**. The earlier file [`85-micron-2015-read-retry-mode-power-boundary-deepening.md`](85-micron-2015-read-retry-mode-power-boundary-deepening.md) deliberately left the L83A `89h`/`FFh` question open. Direct inspection of the same datasheet's **Configuration Operations** section now closes that narrower question. Where the earlier packet says exact L83A reset survival is unproven, this packet supersedes that statement.

Canonical case: [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md).

---

## Scope

The question is intentionally narrow:

> For Micron's May-2015 L83A 32Gb asynchronous/synchronous MLC NAND family, does selecting read-retry feature address `89h` survive the three reset commands documented by that datasheet, and how does that differ from reset of an in-flight operation or from power-down?

The answer is source-bounded:

```text
selected read-retry feature 89h
    survives documented RESET classes FFh / FCh / FAh
    unless an address-specific exception says otherwise

but

power-down
    ends the selected read-retry setting
```

The same source also says RESET cancels pending array operations and invalidates volatile data/cache-register contents. Therefore the strongest retention result is not merely `reset != power cycle`; it is:

```text
operation-progress state can be retired by RESET
    while
read-interpretation feature state survives that RESET
```

This packet does **not** claim that every Micron NAND generation has this behavior, that every feature survives every reset, or that later `Hard Reset (FDh)` semantics can be projected backward onto the L83A family.

---

## Source ledger

### P1 — Micron Technology, L83A 32Gb NAND datasheet, Rev. A, May 2015

Micron Technology, **“32Gb, Asynchronous/Synchronous NAND”**, file identifier `L83A_32Gb_Async_Sync_NAND_mlc_plus.pdf`, PDF ID `09005aef8644c380`, Rev. A **5/15 EN**.

Public mirrors inspected:

- <https://www.farnell.com/datasheets/3761294.pdf>
- <https://www.unikeyic.com/media/datasheet/d9/6b/ded2/d9/8c2c3bd5996175045d2af62c6e827efe.pdf>

Relevant printed pages/sections:

- p. 42 — `RESET (FFh)`;
- pp. 43–44 — `SYNCHRONOUS RESET (FCh)` and `RESET LUN (FAh)`;
- p. 62 — `Configuration Operations` and feature-address reset rule;
- p. 66 — `Feature Address 89h: Read Retry`;
- p. 87 — `Read Retry Operations`.

The document names the L83A family and includes `MT29F32G08CBADA` device/package variants in its parameter-page tables.

### P2 — upstream Linux Micron read-retry support, 14 January 2014

Linux commit `8429bb3975ef81c114cde4da111e64d224d19f83`, **“mtd: nand: support Micron READ RETRY”**:

<https://github.com/torvalds/linux/commit/8429bb3975ef81c114cde4da111e64d224d19f83>

The commit says it was tested on `MT29F32G08CBADA`, reports eight read-retry modes, selects Micron vendor feature address `89h`, and restores mode `0` after the retry sequence.

P2 is a software-artifact/chronology bridge. The reset semantics below come from P1.

### Companion-repository check

`tmzncty/computing-archaeology` was searched for `JFFS2` earlier in this run while evaluating candidate slices, and for Case 85 the repository's existing companion-repo routing was retained: broader NAND command genealogy belongs there if developed. No existing companion packet is being duplicated here.

---

## Historical record

### H-85.51 — the L83A configuration section states a default reset-survival rule for feature addresses

Micron's `Configuration Operations` section says `SET FEATURES (EFh)` and `GET FEATURES (EEh)` modify/read feature-address state. It then gives a general rule:

> unless otherwise specified, feature-address values do not change when host `RESET (FFh, FCh, FAh)` is issued.

The same table on that page explicitly identifies:

```text
89h -> Read Retry
```

This is stronger than inferring reset behavior from the separate read-retry paragraph. It is an exact-family vendor statement covering the feature-address namespace used by read retry.

### H-85.52 — feature `89h` has no reset-specific exception in its table

The `Feature Address 89h: Read Retry` table defines:

- `00h` as disable/default;
- `01h` through `07h` as retry options 1–7;
- one note that a selected option can lengthen `tR`.

The inspected table does not override the Configuration Operations reset-survival rule for `89h`.

Therefore the bounded direct reading is:

```text
SET FEATURES 89h = option N
    -> FFh / FCh / FAh
    -> 89h remains option N
```

subject to the datasheet's own `unless otherwise specified` structure.

This closes the earlier evidence debt for these three reset commands on this family.

### H-85.53 — RESET still retires other state and in-flight work

The same datasheet's `RESET (FFh)` section says the command:

- puts a target into a known condition;
- aborts command sequences in progress;
- discontinues array operations on all die/LUNs during `tRST`;
- cancels pending single- and multi-plane operations;
- can leave an interrupted PROGRAM/ERASE partially programmed/erased and invalid;
- clears the command register;
- invalidates data-register and cache-register contents.

`SYNCHRONOUS RESET (FCh)` is likewise described as aborting in-progress command sequences and invalidating data/cache-register contents while retaining the synchronous interface.

So the phrase `known condition` cannot safely be expanded into `all device state returned to every power-on default`.

The source itself gives a counterexample: feature-address values generally survive these reset classes.

### H-85.54 — power-down is a separate retirement boundary for selected read-retry state

Micron's `Read Retry Operations` section says that once the host writes feature address `89h`, subsequent reads use the associated internal settings until either:

1. `89h` is rewritten; or
2. the device is powered down.

The same section instructs the host to return the retry option to default before the next normal array read once a retry becomes ECC-correctable.

Combining the source's two statements gives a specific event ordering:

```text
write 89h option N
    -> ordinary reads use N
    -> FFh/FCh/FAh does not, by the general feature rule, retire N
    -> explicit 89h rewrite can retire/change N
    -> power-down retires the selected read-retry setting
```

This is an event-class persistence horizon, not a statement that the retry option is nonvolatile storage in the ordinary payload sense.

### H-85.55 — Linux explicitly restores mode 0 rather than depending on reset

The 2014 Linux commit's recommended sequence ends with `SET_FEATURES` feature `89h`, mode `0`, after a retry search.

That is consistent with the later Micron contract: a host should not assume that issuing ordinary NAND RESET will restore the read-retry feature to default.

This does not prove that the Linux implementation was written because of the exact May-2015 wording; the commit predates this document revision.

---

## Engineering reconstruction

### E-85.51 — `reset` is not one universal state-lifetime boundary

The source forces at least four state classes apart:

```text
in-flight array operation
command/data/cache-register state
selected feature-address state
nonvolatile NAND payload state
```

For the bounded L83A behavior:

```text
FFh/FCh/FAh
    can abort in-flight work
    can invalidate register contents
    but generally do not change feature-address values
```

while:

```text
power-down
    ends selected read-retry 89h state
    but does not erase NAND payload merely by being a power-down event
```

Therefore:

> **reset survival is state-class × event-class specific.**

### E-85.52 — operation cancellation and interpretation-state retirement are distinct

A reset may cancel an active NAND operation without changing the read-retry setting that will condition future array reads.

So:

```text
operation aborted
    !=
reader configuration returned to default
```

and:

```text
command register cleared
    !=
feature register cleared
```

This is a useful control-state boundary because both states are volatile in a broad everyday sense, yet they have different documented horizons.

### E-85.53 — `known condition` must be typed

A loose engineering paraphrase might say `RESET returns the NAND to a known state`. The vendor wording supports that phrase only if the state dimensions are kept explicit.

For example, after FFh the host can know that pending array operations were cancelled and that command/data/cache registers are invalidated or reset as described, while separately knowing that feature-address state generally survived.

Thus:

```text
known post-reset protocol condition
    !=
all configuration equals power-on default
```

### E-85.54 — default restoration is an explicit host action in the retry workflow

Because reset does not provide a general `89h -> 00h` transition for this family, the retry workflow's explicit `SET FEATURES 89h = 00h` is not redundant bookkeeping.

It establishes a controlled handoff:

```text
degraded-page interpretation search
    -> successful ECC recovery
    -> explicitly restore normal reader state
    -> subsequent unrelated reads
```

This is **reader-state cleanup**, not representation renewal and not Flash refresh.

### E-85.55 — cross-command persistence, reset survival, and power survival are three different claims

The corrected horizon can be written compactly as:

```text
89h selected option
    persists across subsequent READ commands
    persists across documented FFh/FCh/FAh resets
    does not persist across power-down
```

Hence:

```text
command-to-command persistence
    != reset persistence
    != cross-power persistence
```

The first two happen to be true for this state on this family; the third is not.

---

## Relation to the later Micron `Hard Reset (FDh)` evidence

Case 85 also contains a later Micron patent/design witness, priority 12 January 2018, in which ordinary resets such as `FFh/FCh/FAh` may leave feature `89h` intact while `Hard Reset (FDh)` can restore it to default; custom retry scratch state may live in SRAM and be cleared by `FDh` or power cycle.

The 2015 L83A datasheet now provides direct product-family evidence for the ordinary-reset side:

```text
2015 L83A product contract:
    FFh/FCh/FAh generally preserve feature values, including 89h absent exception

2018-priority design disclosure:
    later examples distinguish those ordinary resets from FDh Hard Reset
```

Safe conclusion:

> a reset-class distinction exists in Micron evidence at both product-contract and later design-disclosure layers.

Unsafe conclusion:

> the 2015 L83A necessarily implements `FDh` with the later patent's exact semantics.

No such projection is made.

---

## Cross-case comparisons

### Case 38 — Intel S3700 feature persistence

Case 38 separates a feature-control mechanism from named-feature persistence and warns against assuming one generic reset horizon. Case 85 now supplies a raw-NAND named-family instance in which ordinary reset survival is directly documented while power-down remains a separate boundary.

Functional comparison only:

```text
feature exists
    !=
feature value's event-specific persistence is known
```

### Case 146 — erase-suspend / pending-operation state

Case 146 distinguishes retained payload/currentness from transient operation microstate. L83A RESET provides a complementary boundary: in-flight array work can be cancelled while a read-interpretation feature persists.

No implementation genealogy is implied.

### Case 149 — OTP authority

Case 149's OTP state is deliberately nonvolatile and can irreversibly retire mutation authority. Case 85's `89h` selection is instead a reset-surviving but power-bounded reader configuration.

The common point is only that control state has a typed persistence horizon; the substrates and semantics differ.

---

## Functional analogy

A bounded analogy is a measuring instrument whose current calibration preset remains selected when an acquisition is aborted/reset, but whose selected preset is lost when the instrument is fully powered down.

That analogy clarifies the distinction between:

- aborting work;
- clearing working buffers;
- retaining configuration;
- losing configuration at a stronger event boundary.

It supplies no NAND evidence and is not a historical genealogy claim.

---

## Philosophical interpretation — downstream only

One restrained interpretation is justified:

> technical discontinuity is not a property of `reset` in the abstract; it is a relation between a named event and a named state class.

On this device family, RESET can terminate an operation without terminating the selected interpretation condition. Power-down has a different boundary. The retained system therefore contains multiple overlapping temporal horizons rather than one global before/after line.

This is project interpretation, not Micron vocabulary.

---

## Explicit non-claims

This packet does **not** claim that:

1. Micron invented read retry or reset-surviving feature registers.
2. the May-2015 datasheet proves identical wording in the pre-2014 datasheets consulted by the Linux author.
3. every Micron NAND family preserves every feature across `FFh/FCh/FAh`.
4. every feature address in the L83A family lacks exceptions; the datasheet explicitly allows address-specific exceptions.
5. feature `89h` survives power-down; the read-retry section states the opposite boundary.
6. feature `89h` is stored in NAND array cells, fuse, EEPROM, SRAM, or any specific physical carrier; the product document does not expose that implementation.
7. ordinary RESET leaves in-flight operation progress intact; the reset section explicitly cancels pending operations.
8. a cancelled PROGRAM/ERASE is safe to resume; the source warns the affected data may be partially programmed/erased and invalid.
9. `RESET puts target into a known condition` means every internal state returns to a power-on default.
10. the 2015 product supports `Hard Reset (FDh)` with the exact semantics of the later 2018-priority patent family.
11. controller reset, PCIe reset, host software restart, NAND `FFh`, NAND `FAh`, and power cycle are interchangeable events.
12. a surviving retry option is the same as durable per-page retry history.
13. successful read retry refreshes, rewrites, relocates, or sanitizes the NAND payload.
14. the Linux mode-0 cleanup proves a commercial SSD firmware follows the same sequence in every context.
15. this correction changes Case 85's maturity beyond `grounded`; it closes one evidence debt only.

---

## What this closes

Closed in this slice:

- exact L83A ordinary-reset relationship for feature `89h` under the datasheet's default feature rule;
- distinction between RESET-aborted operation state and RESET-surviving read-retry configuration;
- direct product-family evidence that `FFh/FCh/FAh` and power-down are different persistence boundaries for read-retry state;
- the earlier repository non-claim that exact 2015 `89h` behavior across `FFh` remained unproven.

Still open:

- direct silicon/logic-analyzer transcript demonstrating `GET FEATURES 89h` before and after each reset class on a real L83A part;
- whether all package/die revisions covered by the family behave identically under undocumented edge cases;
- exact physical carrier of feature state;
- behavior across brownout / partial power-domain collapse rather than specified power-down;
- whether any named managed SSD stores durable page/block retry hints above the raw-NAND feature layer;
- product-level deployment and semantics of later Micron `FDh` Hard Reset.

---

## Bounded conclusion

The 2015 Micron L83A source establishes a sharper persistence hierarchy than the earlier Case 85 packet recorded:

```text
NAND payload state
    -> nonvolatile medium relation

read-retry capability
    -> discoverable device capability

selected 89h retry option
    -> persists across reads
    -> survives documented FFh/FCh/FAh reset classes
    -> ends on explicit rewrite or power-down

in-flight array operation / data-cache-register state
    -> can be cancelled / invalidated by RESET
```

The key result is therefore:

> **RESET can retire operation progress without retiring the reader configuration that will govern later reads.**

That is a source-grounded correction to Case 85's previous open boundary, not a universal NAND rule.