# Evidence 149C — Micron 2012–2015 OTP mode state vs irreversible protection persistence

## Status

**`bounded deepening complete`** — this record deepens Case 149 only at the state-lifetime boundary between **volatile OTP mode selection** and **irreversible OTP protection authority**. It does not attempt to identify the physical lock-cell implementation, prove an invasive-tamper property, or replace the earlier 2004–2006 grounding and ONFI/interface chronology.

Canonical case: [`../cases/149-micron-nand-otp-data-protect-irreversible-authority.md`](../cases/149-micron-nand-otp-data-protect-irreversible-authority.md)

Earlier grounding:

- [`149-micron-2004-2006-nand-otp-data-protect-grounding.md`](149-micron-2004-2006-nand-otp-data-protect-grounding.md)
- [`149-onfi10-20-vendor-feature-space-otp-interface-deepening.md`](149-onfi10-20-vendor-feature-space-otp-interface-deepening.md)

The bounded question is:

> when Micron moved OTP access behind `SET FEATURES` array-operation modes, did the selected OTP/protect mode itself become the durable protection state, or does the product contract separate a short-lived mode selector from a longer-lived irreversible authority relation?

The answer in the inspected Micron product documents is the latter.

---

## Why this slice matters

The earlier Case 149 records already establish that Micron NAND separates:

- OTP payload programming;
- a later protection operation;
- post-protection read access;
- and the absence of an exposed unprotect transition.

The ONFI/interface deepening then showed that later Micron products select OTP behavior through vendor feature address `90h`.

That leaves a potential ambiguity:

```text
feature address 90h = 03h
    ?
    permanent OTP protection state
```

The later product documents make that identification unsafe. The `90h` feature value is an **operation-mode selector** with a bounded lifetime. The actual protected/unprotected relation is established by a separate NAND programming operation and thereafter changes what future program attempts are admitted.

This produces a useful retention distinction:

```text
transient mode-selection state
    !=
retained mutation-authority state
```

---

## Evidence classes used here

- `H/P*` — manufacturer-authored period product document preserved by a third-party host;
- `E` — engineering reconstruction from explicitly documented relations;
- `A` — bounded functional analogy to another repository case;
- `I` — project-level interpretation;
- `X` — rejected shortcut / stop condition.

No philosophical label is treated as historical vocabulary.

---

## Source ledger

### S1 — Micron 4Gb / 8Gb / 16Gb x8/x16 NAND Flash Memory, Rev. N 10/12 (`H/P*`)

- Manufacturer: Micron Technology, Inc.
- Document family includes `MT29F4G08ABADAH4`, `MT29F4G08ABADAWP`, `MT29F8G08ADADAH4`, `MT29F16G08AJADAWP`, and related x8/x16 variants.
- File identifier: `09005aef83b25735`.
- Document file name: `m60a_4gb_8gb_16gb_ecc_nand.pdf`.
- Revision: **Rev. N 10/12 EN**.
- Preserved manufacturer PDF on Texas Instruments E2E infrastructure: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/5355.nand_5F00_datasheet.pdf>

Why `H/P*`: the PDF is Micron-authored period product documentation, but this run did not recover the same revision from an origin-hosted Micron URL.

Relevant records:

1. `SET FEATURES (EFh)` / `GET FEATURES (EEh)` modify target feature state.
2. The document says a set feature is **volatile by default** and remains active until the device is power-cycled unless otherwise specified.
3. Feature address `90h` is `Array operation mode`.
4. `P1=00h` selects normal mode, `P1=01h` selects OTP operation, and `P1=03h` selects OTP protection mode.
5. The table note says these `90h` mode bits are reset to `00h` on power cycle.
6. The OTP section separately says the device enters OTP protect mode first, then executes the documented program sequence against the OTP protect page.
7. After good completion, protected OTP pages cannot be programmed further and cannot be unprotected.
8. A repeated protect request after the OTP area is already protected produces the documented protected/write-protected status behavior.
9. OTP data remains readable whether the area is protected or not, after selecting the proper OTP operation mode.

### S2 — Micron 32Gb Asynchronous/Synchronous NAND, Rev. A 5/15 (`H/P*`)

- Manufacturer: Micron Technology, Inc.
- Named device witness: `MT29F32G08CBADBWPR:D` and associated L83A family variants.
- File identifier: `09005aef8644c380`.
- Document file name: `L83A_32Gb_Async_Sync_NAND_mlc_plus.pdf`.
- Revision: **Rev. A 5/15 EN**.
- Preserved manufacturer PDF: <https://datasheet.lcsc.com/lcsc/1908271118_Micron-Tech-MT29F32G08CBADBWPR-DTR_C410864.pdf>

Why `H/P*`: manufacturer-authored product data, currently retrieved from a distributor mirror rather than a Micron-origin URL.

Relevant records:

1. feature address `90h` remains `Array operation mode`;
2. `00h` is normal/default and `01h` selects the OTP block in this family;
3. the `90h` array-operation-mode bits return to default when `RESET (FFh)` is issued; in synchronous mode, `SYNCHRONOUS RESET (FCh)` also returns them to default;
4. the OTP section explicitly says `RESET (FFh)` while in OTP operation mode exits OTP operation mode and returns the target to normal operating mode;
5. `SYNCHRONOUS RESET (FCh)` likewise exits OTP operation mode while retaining the synchronous interface;
6. OTP protection is nevertheless a separate `PROTECT OTP AREA (80h-10h)` programming operation directed at the OTP protect-page address;
7. after the OTP area is protected, normal OTP programming no longer succeeds and the document says the area cannot be unprotected.

S2 is not used to claim that the 2015 L83A family uses the same internal protection representation as S1 or the 2006 Case-149 product witness. It is a later same-vendor product-contract witness showing the same analytical separation between mode state and protection state.

### S3 — same-device block-lock section in S1 (`H/P*`, negative control)

The S1 device family also documents ordinary main-array block locking and `LOCK TIGHT (2Ch)`.

The important negative control is that `LOCK TIGHT` cannot be disabled by a software command, **but power cycling disables the lock-tight status**; after that transition, blocks become locked as if the ordinary lock command had been issued.

This matters because it blocks a terminology shortcut:

> `cannot be disabled by software` does not automatically mean `survives power cycle`.

Micron uses different contracts for different protection mechanisms on the same NAND device family.

---

## Historical / implementation record

### 1. `SET FEATURES` state is explicitly volatile in the 2012 product contract

S1 describes the feature mechanism as changing target behavior and says that, by default, a set feature remains active until power cycle and is **volatile**.

That establishes a generic horizon for feature state:

```text
SET FEATURES value
    -> effective runtime/device configuration
    -> power-cycle boundary
    -> default configuration restored
```

This is not yet specific to OTP, but feature address `90h` supplies the specific mapping.

### 2. Feature address `90h` selects an array-operation mode

For S1, feature address `90h` P1 maps:

```text
00h -> normal
01h -> OTP operation
03h -> OTP protection mode
```

and the table note explicitly says those bits reset to `00h` on power cycle.

Therefore:

> **OTP-protection mode selected != permanent protection state established**.

If the value `03h` itself were the permanent protection state, returning that field to `00h` on every power cycle would amount to an exposed unprotect transition. But the same product document explicitly says the protected OTP area cannot be unprotected.

The safe reading is that `03h` selects the **context in which the protection operation is to be performed**; it is not the irreversible protected/not-protected state itself.

### 3. Entering protect mode is only a prerequisite to the irreversible operation

S1's OTP section tells the host to enter OTP protect mode through feature address `90h`, then issue the program sequence directed at the OTP protect page.

The sequence is conceptually:

```text
SET FEATURES 90h -> P1=03h
        |
        v
OTP protect mode selected
        |
        v
PROGRAM sequence to OTP protect page
        |
        v
busy / status qualification
        |
        v
protected relation established after good status
```

Thus:

> **mode selection != operation completion**

and

> **operation request != protected state**.

This is the same completion boundary already visible in the 2006 grounding, now shown under the later feature-address interface.

### 4. Power-cycle forgetting of the selector does not restore future program authority

S1 says two things that must be interpreted together:

- `90h` operation-mode bits return to `00h` on power cycle;
- once OTP data has been protected, the pages are no longer programmable and cannot be unprotected.

The product contract therefore contains two persistence horizons:

```text
volatile access / operation selector
    power-cycle horizon

irreversible protected/unprotected relation
    no exposed unprotect transition
```

This record does **not** claim a laboratory power-cycle experiment was performed. It records the product contract and its internal distinction.

A future hardware test remains useful because interface documentation does not reveal the physical encoding, redundancy, or failure behavior of the retained protection state.

### 5. Re-entering an OTP mode after reset/power cycle is compatible with permanent protection

The mode selector controls where ordinary NAND read/program operations are routed or which special operation is being requested. Losing that selector does not imply losing the OTP payload or its protection relation.

Operationally, later software can re-establish an access context:

```text
power cycle / reset
    -> normal array-operation mode
    -> host explicitly selects OTP operation mode again
    -> OTP data can be read
    -> if area had been protected, further programming remains disallowed by the protection contract
```

This yields:

> **access context must be reconstructed != retained object was forgotten**.

### 6. The 2015 family makes the reset boundary even more explicit

S2 says a normal `RESET (FFh)` while in OTP operation mode exits OTP operation mode and returns the target to normal operating mode. Its array-operation-mode table also says reset returns those mode bits to default.

That gives a clean reset-level example:

> **reset destroys/clears mode-selection state != reset destroys protected OTP state**.

Again, the second half is a contract-level conclusion from the absence of an unprotect transition and the separate protect-page programming operation, not a disclosed circuit diagram.

### 7. Same vendor, same device, different protection horizons

S1's block-lock mechanism is a useful internal control. `LOCK TIGHT` is stronger than ordinary software unlock while it is active, yet the document explicitly says power cycle disables the lock-tight status.

OTP protection, by contrast, is documented as not unprotectable.

Therefore:

```text
software-unlockable during current power epoch
    !=
permanently retired program authority
```

The word `lock`, `protect`, or `tight` is not enough to infer persistence horizon. The actual reset/power contract must be read.

---

## Engineering reconstruction

### A. Split the state machine into selector and authority planes

A useful reconstruction is:

```text
Plane 1 — volatile operation selector

normal (00h)
  <-> OTP operation (01h)
  <-> OTP protect mode (03h)

power cycle -> normal/default
reset behavior -> family-specific documented defaulting


Plane 2 — retained OTP authority relation

unprotected
   |
   | successful protect-page programming
   v
protected

protected -> unprotected
    [no documented transition]
```

The two planes interact, but they are not the same state variable.

### B. Mode state is routing / command-context state

The feature selector determines how following operations are interpreted:

- normal array operations target the ordinary array;
- OTP operation mode routes supported read/program operations to OTP pages;
- OTP protect mode enables the sequence that establishes the one-way protection relation.

It is therefore better modeled as **operation context** than as the protected relation itself.

### C. Protection authority is history-sensitive

After successful protect-page programming, future admissible operations depend on a fact about prior history:

```text
was successful OTP protection established earlier?
```

That relation must remain available to the device after the volatile command context is gone, otherwise the statement `cannot be unprotected` would not be meaningful across normal power use.

The exact physical state used to answer that question remains undisclosed in the inspected product documents.

### D. Retained prohibition can outlive the state used to establish it

This case provides a compact example of:

```text
transient authority-establishment context
    -> irreversible transition
    -> context disappears
    -> transition result remains authoritative
```

Comparable software examples exist, but no software ancestry is implied. The important engineering form is simply that **the mechanism used to request a durable transition need not itself be durable**.

---

## Failure and boundary matrix

| Boundary | `90h` mode selector | OTP payload | OTP protection authority | Safe conclusion |
| --- | --- | --- | --- | --- |
| ordinary command progress | active according to current feature setting | retained | retained if already established | command context and retained data are separate |
| explicit return to normal mode | selector becomes normal | retained | no documented unprotect | leaving mode is not unprotecting |
| power cycle in S1 | selector bits reset to `00h` | NAND payload expected to persist under product retention contract | no exposed unprotect transition | selector volatility does not imply authority volatility |
| `RESET (FFh)` in S2 | OTP operation mode exits / defaults | retained outside an interrupted program caveat | no exposed unprotect transition | reset of mode is not documented as reset of protection |
| interrupted protect programming | completion not proven | may require device-specific handling | protected state must not be assumed without good status | command issue is not enough |
| post-protect program attempt | host can request after re-entering suitable context | existing payload readable | programming rejected by documented protected-state behavior | protection changes future admissibility |

The row for interrupted protection is intentionally conservative: the inspected sources specify success qualification but this record does not infer a fully crash-atomic protection transition under arbitrary power loss during `tPROG`.

---

## Same-device negative control: block lock

S1 makes the terminology lesson unusually strong because the same product family also has a different locking mechanism.

`LOCK TIGHT`:

- cannot be disabled by software while active;
- nevertheless has a documented power-cycle transition that disables the tight status;
- leaves blocks locked after that transition.

OTP protection:

- is established through OTP protect-page programming;
- makes OTP pages no longer programmable;
- has no documented unprotect operation.

This means a repository-level vocabulary should avoid collapsing all of the following into `write protected`:

```text
ephemeral mode selection
software-non-unlockable state within a power epoch
power-cycle-modified lock state
irreversible OTP mutation-authority retirement
```

They have different horizons and different restoration rules.

---

## Cross-case comparison

### Case 85 — Micron NAND Read Retry (`A`)

Case 85 recently grounded a Micron read-retry selection whose active retry setting is temporary and can be forgotten at the device's power boundary.

Case 149 adds an important contrast from the same broad raw-NAND configuration world:

```text
read-retry / operation-mode selection
    may be intentionally temporary

OTP protection authority
    intentionally survives the temporary selector used to establish/access it
```

Safe conclusion:

> **same `SET FEATURES` style control plane != same persistence horizon for the state ultimately relevant to recoverability or mutation authority**.

No claim is made that read-retry and OTP protection share an internal implementation.

### Synthesis 29 — semantic persistence and restart continuation (`A`)

Synthesis 29 separates retained scalar/bit state from the interpretation frame needed to preserve its meaning across restart.

Case 149 contributes a complementary shape: sometimes the **interpretation/access mode may be deliberately reconstructed**, while the underlying authority relation remains durable.

That is not a contradiction. It means restart analysis should ask which layer needs persistence and which layer is intended to be reselected.

### Case 114 — NVMe namespace write protection (`A`)

Both cases restrict future writes, but the authority substrate and reset semantics differ. Case 149 is a raw-NAND OTP area with a one-way protect operation; namespace write protection is a controller/namespace policy contract.

The shared functional phrase `write protection` does not establish equivalent persistence horizons.

---

## Historical record vs engineering reconstruction vs analogy vs philosophy

### Historical / implementation record

The Micron documents actually say:

- feature values are volatile by default;
- feature address `90h` selects normal / OTP operation / OTP protection context in S1;
- `90h` mode bits reset on power cycle in S1;
- later S2 resets/exits OTP operation mode on `FFh`/`FCh` as documented;
- OTP protection requires a separate protect-page programming operation;
- successful protection makes the OTP area non-programmable and not unprotectable;
- OTP data remains readable;
- S1 block-lock tightness has a different power-cycle rule.

### Engineering reconstruction

This repository reconstructs those statements as two different state layers:

1. volatile operation-selector state;
2. retained mutation-authority state.

That reconstruction is narrower than a claim about exact transistor-level embodiment.

### Functional analogy

Comparisons to read-retry, NVMe namespace write protection, or restart-persistence frameworks are used to sharpen the persistence-horizon distinction only.

### Philosophical interpretation

A later philosophical reading might say that an irreversible rule can outlive the temporary procedure that instituted it. That is **project interpretation**, not Micron vocabulary and not evidence of designer intent.

---

## Explicit non-claims

This record does **not** claim:

1. that Micron invented NAND OTP;
2. that the 2012 or 2015 product families use the exact 2006 protection circuitry;
3. that feature address `90h` is an ONFI-standard OTP semantic assignment;
4. that `P1=03h` is itself the nonvolatile protection bit;
5. that resetting `P1` to `00h` erases or unprotects OTP data;
6. that an OTP protect request is complete before status says it completed successfully;
7. that arbitrary power failure during protect programming is crash-atomic;
8. that the exact physical encoding of protection state is disclosed;
9. that protection survives invasive fault injection or semiconductor reverse engineering;
10. that OTP protection provides confidentiality;
11. that OTP protection is secure erase or sanitization;
12. that `cannot be unprotected` means no laboratory technique can ever alter the cells;
13. that every Micron NAND family uses the same page geometry or feature values;
14. that all `SET FEATURES` state is cleared by all reset commands on all families;
15. that a power-cycle rule from S1 should be back-projected into the 2006 dedicated-opcode product;
16. that S2's reset behavior proves the same reset behavior for S1;
17. that `LOCK TIGHT` and OTP protection are implementation relatives merely because they coexist in one datasheet;
18. that a software lock, cloud WORM policy, and NAND OTP lock are the same mechanism;
19. that read-retry state and OTP protection share an internal latch or storage cell;
20. that a product-document contract substitutes for a physical-device experiment.

---

## Claim ledger

| Claim | Evidence class | Source | Strength |
| --- | --- | --- | --- |
| S1 `SET FEATURES` state is volatile by default until power cycle | `H/P*` | S1 | strong product-document claim |
| S1 feature address `90h` selects normal / OTP operation / OTP protect modes | `H/P*` | S1 | strong product-document claim |
| S1 `90h` mode bits reset to `00h` on power cycle | `H/P*` | S1 | explicit table note |
| S1 requires a separate protect-page program sequence after entering protect mode | `H/P*` | S1 | explicit procedure |
| successful OTP protection prevents further programming and cannot be undone through the documented interface | `H/P*` | S1 | explicit product contract |
| S2 reset exits/defaults OTP operation mode | `H/P*` | S2 | explicit product contract |
| mode selector and protection authority are distinct state layers | `E` | S1 + S2 | strong reconstruction from conflicting lifetimes |
| power-cycle forgetting of selector is not an unprotect operation | `E` | S1 | strong contract-level reconstruction, not a hardware test |
| `LOCK TIGHT` demonstrates that software-non-disableable does not imply power-persistent | `H/P*` / `E` | S1 | strong same-device negative control |
| exact protection-state circuitry | `X` | none | unresolved |
| crash-atomicity of a power failure during protect programming | `X` | none | unresolved |

---

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `Micron OTP NAND protect 90h` and `OTP DATA PROTECT` returned no dedicated packet to reuse.

This record therefore stays in `technical-retention` because its bounded question is not the broad history of NAND OTP. It is the retention-specific seam:

> **a volatile command/access context can establish or expose a durable authority relation without being the durable relation itself**.

A wider history of:

- Micron NAND generation transitions;
- cross-vendor OTP/security-register command design;
- ONFI committee evolution;
- internal lock-cell circuits;
- physical attacks and fault injection;
- controller-driver adaptation;

belongs primarily in `computing-archaeology` if developed later.

---

## What this closes

This packet closes the narrow Case-149 debt around **documented reset/power-boundary semantics of the later feature-address OTP interface** to the following bounded answer:

- Micron's later `90h` OTP/protect mode selection is not itself the permanent protection state;
- at least the inspected 2012 family explicitly resets the `90h` mode bits to normal on power cycle;
- the inspected 2015 family explicitly exits/defaults OTP operation mode on reset;
- protection is established by a separate status-qualified program operation;
- the product contract then provides no unprotect transition and rejects further OTP programming;
- therefore operation-mode reconstruction and protection-authority persistence are separate responsibilities.

This does **not** close the hardware-validation debt.

---

## Remaining debt

- obtain an origin-hosted archival Micron copy of S1/S2 or equivalent revisions where possible;
- identify the exact physical protection-state representation for a named shipped die if public reverse-engineering or manufacturer evidence exists;
- perform a compatible-device experiment that programs test OTP data, protects it, power-cycles/resets the device, re-enters OTP mode, verifies readback, and records post-protect program rejection;
- test interruption during the protection `tPROG` window only under a deliberately bounded destructive experiment, because the documents here do not establish crash-atomicity;
- keep broader NAND OTP / security-register genealogy in `computing-archaeology` rather than duplicating it here.
