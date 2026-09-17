# Case 85 Deepening — Micron 2015 Read-Retry Mode Lifetime and Power Boundary

**Case:** [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md)  
**Status:** `bounded deepening complete`  
**Question:** for a named Micron MLC NAND family, which parts of read-retry are durable/discoverable device capability and which parts are only the currently selected reader state, and what happens to that selected state at the power boundary?

---

## 1. Why this slice exists

The existing Case 85 evidence established two things from upstream Linux:

1. the 2014 Micron driver obtained a read-retry mode count from Micron vendor data and selected retry modes through feature address `89h`;
2. the driver returned the NAND to retry mode `0` after the retry sequence.

That was strong software-artifact evidence, but it deliberately left a vendor-primary debt: the Linux commit said it had checked Micron datasheets, while the repository had not itself inspected a Micron document for the exact device family.

This slice closes a bounded part of that debt with a Micron-authored 2015 datasheet for the **32Gb L83A asynchronous/synchronous MLC NAND family**, which includes `MT29F32G08CBADA` variants. The surviving public copy is third-party hosted, so source provenance is:

```text
primary document content: Micron Technology datasheet
    !=
current hosting provenance: independent public mirror
```

The document identifies itself as:

- **32Gb, Asynchronous/Synchronous NAND**;
- PDF identifier `09005aef8644c380`;
- file name `L83A_32Gb_Async_Sync_NAND_mlc_plus.pdf`;
- **Rev. A 5/15 EN**;
- © 2015 Micron Technology, Inc.

This is later than the 2014 Linux merge. It is therefore a direct vendor witness to the device-family contract by 2015, **not** proof that every sentence already appeared in exactly the same form in the datasheet consulted by the Linux author in 2013/2014.

---

## 2. Source ledger

### Source A — Micron L83A 32Gb NAND datasheet, Rev. A, May 2015

Micron Technology, **“32Gb, Asynchronous/Synchronous NAND”**, `L83A_32Gb_Async_Sync_NAND_mlc_plus.pdf`, Rev. A 5/15 EN, PDF ID `09005aef8644c380`.

Publicly recovered mirror used for this slice:

- <https://www.unikeyic.com/media/datasheet/d9/6b/ded2/d9/8c2c3bd5996175045d2af62c6e827efe.pdf>

Relevant printed sections/pages in the document:

- parameter-page read-retry capability fields: printed pp. 53 and 59;
- `Feature Address 89h: Read Retry`: printed p. 66;
- `Read Retry Operations`: printed pp. 87–88.

The document's JEDEC parameter-page table names `MT29F32G08CBADA` / package variants in the device-family rows, so this is not merely a generic Micron NAND application note.

### Source B — upstream Linux Micron read-retry commit, 2014

Upstream Linux commit:

- `8429bb3975ef81c114cde4da111e64d224d19f83`
- **“mtd: nand: support Micron READ RETRY”**
- merged/recorded 2014-01-14
- <https://github.com/torvalds/linux/commit/8429bb3975ef81c114cde4da111e64d224d19f83>

The commit says it was tested on `MT29F32G08CBADA`, with **8 read-retry modes**, and reports Micron vendor-table byte 180 as `08h` for that part.

Source B is used only as an implementation/chronology bridge. The vendor semantics below come from Source A.

### Companion-repository check

`tmzncty/computing-archaeology` was searched again for `read retry Micron NAND`. No dedicated existing history packet was found. Broad NAND-command genealogy still belongs there if developed later; this record remains limited to the retention/control-state boundary.

---

## 3. Historical / implementation record — capability is explicitly enumerated

### 3.1 Micron exposes the number of retry options as parameter-page data

The 2015 Micron document's ONFI parameter-page definition includes:

- byte **180**: `Read Retry options`;
- bits `[3:0]`: number of read-retry options supported;
- value **`08h`** for this family.

It immediately follows with bytes **181–184**, which encode which read-retry options are available as a bit set.

The later JEDEC parameter-page block in the same document similarly contains a vendor-specific read-retry option count and availability map.

The safe historical statement is therefore:

> By the Micron 2015 L83A family datasheet, read-retry capability was a machine-readable device property rather than something a host had to infer only by trial and error.

This also independently supports the shape reported by the 2014 Linux commit:

```text
reported Linux vendor byte 180 = 08h
    <->
2015 Micron family parameter page = 08h
```

The arrow is corroboration, not proof that the 2015 document caused the 2014 patch.

### 3.2 Capability count and currently active mode are separate states

Micron's configuration table defines feature address `89h` with P1 values:

- `00h` — Read Retry Disable (**default**);
- `01h` through `07h` — Options 1 through 7.

Combined with the parameter-page count, this makes two distinct state questions visible:

```text
how many / which retry options does this NAND support?
    !=
which retry option is active right now?
```

The first is discoverable capability metadata. The second is mutable runtime feature state.

---

## 4. Historical / implementation record — retry mode has command-to-command lifetime

### 4.1 SET FEATURES changes later reads, not only one immediate transaction

The `Read Retry Operations` section states that retry is coordinated through NAND reads plus `SET FEATURES (EFh)` at feature address `89h`.

If a page exceeds the ECC correction threshold, the host selects a retry option and performs another array read. If errors remain beyond the ECC threshold, the host selects another option and repeats until either:

- the data becomes correctable; or
- the final retry option is exhausted.

This is not merely a parameter attached to one command packet. The document states that after the host writes the read-retry feature address, **subsequent reads use the internal NAND settings associated with that value** until the feature value is changed or power is removed.

Thus the selected mode is a bounded form of runtime-retained control state:

```text
SET FEATURES 89h = option N
    -> READ
    -> READ
    -> ...
    -> option N remains the reader condition
       until an explicit state-ending event
```

The state persists across subsequent read commands without rewriting user payload.

### 4.2 Correctable-now does not imply the mode should remain selected

The same section says that once the re-read becomes correctable within ECC limits, the read-retry option should be returned to its default before the next NAND array read.

The 2014 Linux behavior of restoring mode `0` therefore matches a later Micron-primary contract shape:

```text
retry search succeeds
    -> logical data becomes recoverable
    -> reader state is restored to default
```

This relation is important because it prevents a false conclusion:

> a retry mode that worked for one degraded page is not thereby established as the correct global read condition for later unrelated pages.

This is a control-lifetime statement, not a claim about how a commercial SSD firmware caches successful per-page read conditions internally.

---

## 5. Historical / implementation record — power terminates the selected retry state

The most useful new retention boundary in Source A is explicit: the selected read-retry setting governs subsequent reads until either:

1. the read-retry feature address is rewritten; or
2. **the device is powered down**.

That gives a clear lifecycle distinction:

```text
runtime command-to-command continuity
    !=
cross-power continuity
```

and:

```text
read-retry capability remains discoverable as a device property
    !=
last selected read-retry option survives a power cycle
```

This is the opposite of a persistent per-page recovery hint. The device contract makes the **active option power-bounded**.

The power boundary is especially useful for this repository because NAND user payload is nonvolatile while this interpretation/control state is not guaranteed to cross the same boundary.

Therefore, on one physical device:

```text
user payload threshold distributions
    can outlive power

while

currently selected read-retry option
    is terminated by power-down
```

The two state classes have different persistence horizons even though both participate in whether the payload is readable at a particular moment.

---

## 6. RESET is deliberately left as a separate evidence question

This slice does **not** silently equate `power-down` with every possible `RESET (FFh)` event.

The Micron document explicitly discusses reset behavior for some other feature state, such as timing/data-interface mode, and that behavior can depend on interface mode. That is enough to show that reset semantics are feature-specific and should not be guessed from a power-cycle statement.

For feature address `89h`, the safe direct claim from the read-retry section is only:

- the option remains active for subsequent reads;
- rewriting `89h` can replace/end that option;
- power-down ends the stated lifetime.

Whether every form of `RESET (FFh)`, target reset, controller reset, or partial power-domain reset returns `89h` to `00h` is **not independently closed here**.

This distinction matters because:

```text
power-cycle boundary
    !=
generic reset boundary
    !=
host-controller software restart boundary
```

unless a source explicitly equates them.

---

## 7. Engineering reconstruction — persistence horizons inside one recovery mechanism

The combined Micron/Linux evidence supports at least four different horizons.

### Layer A — physical payload state

The NAND threshold distributions are nonvolatile storage state. Read retry does not itself rewrite them.

### Layer B — device capability description

The host can discover the number/availability of read-retry options from parameter data. This describes what retry states the device supports.

The source does not require the repository to speculate about the exact physical carrier of that metadata; the relevant operational fact is that it is exposed as device-identifying/capability data.

### Layer C — currently selected read-retry option

Writing feature `89h` selects internal read settings used by following reads.

This state:

- persists across subsequent reads;
- is mutable by another feature write;
- is terminated at power-down according to the vendor text.

### Layer D — higher-layer remembered recovery advice

A controller or FTL could separately remember that option N worked well for a certain block/page/word line and select it again later.

Neither the 2015 Micron raw-NAND datasheet nor the 2014 Linux path proves such durable per-page history.

Thus:

```text
device mode persists across commands
    !=
host remembers mode across software restart
    !=
controller stores per-page retry history
    !=
mode survives NAND power loss
```

These are four different claims and need four different witnesses.

---

## 8. Engineering reconstruction — capability persistence is not selected-state persistence

A common loose sentence would be: `the NAND supports eight retry modes, so the retry state is persistent.`

The Micron document shows why that is too coarse.

The device may continue to be a member of a family that exposes eight modes after every initialization, while a particular invocation's selected option is transient.

Project reconstruction:

```text
capability identity
    !=
configuration state
```

More specifically:

```text
reconstructible set of admissible reader states
    !=
currently instantiated reader state
```

This is a concrete Flash example of the broader repository rule that the persistence of a **type of authority/capability** does not imply persistence of a **particular runtime choice** made under that capability.

---

## 9. Engineering reconstruction — reader-state forgetting can be correct behavior

In many retention cases, forgetting control state is a failure. Here, deliberate forgetting/restoration is part of correct operation.

Micron's flow expects a successful retry to be followed by restoring the default read-retry state before the next normal array read.

Therefore:

```text
control-state forgetting
    !=
always a retention defect
```

Sometimes a state has a deliberately bounded lifetime because retaining it too broadly would apply a page-specific recovery condition outside the context that justified it.

The engineering requirement is not `retain everything`. It is:

> retain or reconstruct each state for the horizon over which its meaning and authority remain valid.

This is an engineering reconstruction from the mode-lifetime contract, not Micron's terminology.

---

## 10. Cross-case comparison — Case 36 maintenance time and Case 85 retry mode have different horizons

Case 36 recently established an Intel Flash-maintenance design in which elapsed-time control state can be stored nonvolatilely and reloaded after a power cycle.

Case 85 Micron read retry provides a useful counterexample:

```text
Case 36 maintenance timer:
    design can preserve control history across power

Case 85 selected retry mode:
    vendor contract explicitly ends selected mode at power-down
```

Functional comparison only:

> not all maintenance/interpretation state needs the same persistence horizon.

This does **not** imply that Micron read-retry mode and Intel refresh elapsed time are the same mechanism or share a genealogy.

---

## 11. Cross-case comparison — Synthesis 29 semantic persistence

Synthesis 29 separates several questions that a single label such as `persistent state` would otherwise collapse:

- does the obligation/capability survive?
- does exact progress survive?
- does the interpretation frame survive?
- does restart authority survive?

This Micron source supplies a small but sharp additional pattern:

```text
interpretation capability survives / is rediscoverable
    while
selected interpretation state is power-bounded
```

After power returns, a reader does not need the NAND itself to remember the last retry option in order for read retry to remain a supported operation. It can rediscover capability and run a new retry search.

That is functional comparison, not evidence that Synthesis 29 vocabulary was used historically by Micron.

---

## 12. Cross-case comparison — Case 10 self-refresh authority

Case 10 distinguishes mode-entry authority, cadence authority, coverage authority, and restoration execution in DRAM/LPDDR.

Case 85 adds a different authority split:

```text
host/controller chooses retry option
    -> NAND uses associated internal read settings
    -> power-down retires the selected option
```

Both cases show that `device performs an internal mechanism` does not by itself identify who chooses the mode or how long that choice remains valid.

No DRAM/NAND historical genealogy is asserted.

---

## 13. Functional analogy boundary

A bounded functional analogy is a receiver with several calibration presets:

- the hardware permanently supports a set of presets;
- one preset can remain active across several measurements;
- power loss may clear the selected preset;
- software can select a preset again after restart.

The analogy illustrates:

```text
available state space
    !=
current point in that state space
```

It supplies no historical or device-level evidence and should never replace the Micron NAND source.

---

## 14. Philosophical interpretation — bounded

The narrow philosophical result is not that data become `subjective` because a read threshold changes.

It is only:

> operational retention can depend on a relation between a durable substrate and an intentionally short-lived interpretation state.

A technical system may preserve the physical trace for years while allowing the current reader configuration to vanish at each power boundary. Recoverability can still continue because the reader configuration is **reconstructible**, not because that exact configuration is itself nonvolatile.

So:

```text
continuity of function
    does not require
bitwise continuity of every participating control state
```

provided the required relation can be re-established when needed.

This is a philosophical interpretation of the engineering relation, not a vendor claim.

---

## 15. Explicit non-claims

This slice does **not** claim that:

1. Micron invented NAND read retry.
2. the 2015 datasheet is the first Micron document to describe read retry.
3. the 2015 datasheet proves the exact wording of a 2012, 2013, or early-2014 datasheet.
4. the 2015 document caused the 2014 Linux implementation.
5. the public mirror is a Micron-operated archive; the document content is Micron-authored, but the present host is third-party.
6. ONFI standardizes Micron feature address `89h` as a universal cross-vendor retry address.
7. every NAND family has eight retry options.
8. every Micron NAND has eight retry options.
9. every retry option maps to one simple externally specified threshold-voltage offset; the document exposes option indices and internal settings, not a universal analog-voltage table here.
10. selecting a retry option rewrites user payload.
11. selecting a retry option refreshes threshold distributions.
12. power-down erases user data; it terminates the selected retry-feature state while the NAND payload is nonvolatile.
13. every reset event is equivalent to power-down for feature `89h`.
14. `RESET (FFh)` behavior for feature `89h` is fully established by this slice.
15. host software restart necessarily resets NAND feature `89h`.
16. a successful retry option is permanently appropriate for the same page.
17. Linux persistently stores which retry option succeeded for each page.
18. a commercial SSD FTL exposes the raw-NAND feature exactly as Linux does.
19. rediscoverable capability metadata and active option state have the same physical storage representation.
20. returning to option `00h` repairs or renews media.
21. losing the active option at power-down makes the payload unrecoverable; the host can establish retry state again.
22. this evidence closes the broader genealogy of hard-decision retry, soft reads, or LDPC assistance.

---

## 16. Claim ledger

| Claim | Class | Evidence strength | Boundary |
|---|---|---:|---|
| Micron L83A 32Gb family document exposes a read-retry option count in parameter data | historical/vendor record | strong | Micron-authored 2015 document recovered from third-party mirror |
| the count is `08h` for the documented family | historical/vendor record | strong | document table |
| the document separately enumerates option availability | historical/vendor record | strong | parameter-page table |
| feature address `89h` selects Read Retry Disable/default or retry options | historical/vendor record | strong | configuration table |
| a selected retry option governs subsequent reads | historical/vendor record | strong | Read Retry Operations section |
| selected retry state ends when `89h` is rewritten or device is powered down | historical/vendor record | strong | explicit vendor wording |
| after a correctable retry, the next retry option should be returned to default before the next NAND array read | historical/vendor record | strong | explicit vendor flow |
| Linux 2014 reports the exact `MT29F32G08CBADA` as tested with 8 modes | historical/software artifact | strong | upstream commit |
| 2015 vendor data corroborates the state shape reported by 2014 Linux | engineering/historical comparison | strong | later vendor document; no causal/genealogical claim |
| retry capability metadata and active retry mode have different persistence semantics | engineering reconstruction | strong | capability table + mutable feature lifetime |
| runtime continuity across commands does not imply cross-power continuity | engineering reconstruction | strong | explicit power-down boundary |
| a recovery relation can be reconstructed after power loss without preserving the previous runtime option | engineering reconstruction | moderate/strong | capability rediscovery + power-bounded mode; actual host strategy varies |

---

## 17. Remaining evidence debt

This slice closes a **later vendor-primary exact-family witness** for the Micron control-state model and the power lifetime of selected retry mode.

Still open:

- recover the **pre-2014 / 2014-era revision** of the exact `MT29F32G08CBADA` datasheet that Brian Norris consulted, so chronology does not rely on a 2015 revision for vendor-primary wording;
- determine the exact reset semantics of feature `89h` for this family from a direct vendor clause rather than inferring from the power-down statement;
- recover a Hynix-primary document for the 1x-nm MLC retry-OTP format and the reported recommendation to copy that calibration area;
- trace NAND-core read-retry interface genealogy before/after the 2014 and 2017 vendor implementations;
- obtain commercial SSD firmware/controller evidence for persistent successful-read history, if such history is claimed in a future case;
- keep broad vendor-command genealogy in `tmzncty/computing-archaeology` rather than duplicating it here.

---

## 18. Completion decision

This is a **bounded deepening**, not a new case and not a maturity promotion.

It adds a vendor-primary family-level contract that was missing from the Linux-only deepening:

```text
supported retry state space
    != currently selected retry state

selected retry state persists across reads
    != selected retry state persists across power

payload nonvolatility
    != reader-configuration nonvolatility
```

Case 85 should remain **`grounded`**. The pre-2014 Micron revision, reset-specific behavior, Hynix-primary calibration source, and commercial SSD history remain open.