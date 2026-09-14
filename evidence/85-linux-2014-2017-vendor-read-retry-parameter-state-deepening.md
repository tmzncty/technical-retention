# Case 85 Deepening — Linux 2014–2017 Vendor Read-Retry Parameter State

**Case:** [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md)  
**Status:** `bounded deepening complete`  
**Question:** once read retry is implemented in a general raw-NAND software stack, what control/calibration state must be known or recovered, and how much of that state is vendor-specific rather than standardized by the generic NAND interface?

---

## 1. Claim discipline

This record is deliberately narrower than a history of NAND read retry.

It uses two **upstream Linux implementation commits** as software-artifact evidence:

- Micron read-retry support merged in 2014;
- Hynix 1x-nm MLC read-retry support merged in 2017.

The evidence classes are kept separate:

- **Historical / implementation record:** what those commits say and implement.
- **Engineering reconstruction:** what retained/control relations follow from the code path.
- **Functional comparison:** comparisons to other technical-retention cases.
- **Philosophical interpretation:** only the narrow implication for operational availability.

A Linux driver commit is not silently promoted into a Micron or Hynix datasheet. Where the commit reports vendor behavior or recommendations, this file attributes that statement to the Linux implementation record unless a vendor-primary document was independently checked.

---

## 2. Source ledger

### Source A — Linux Micron read-retry support, 2014

Upstream Linux commit:

- `8429bb3975ef81c114cde4da111e64d224d19f83`
- **`mtd: nand: support Micron READ RETRY`**
- repository timestamp: **2014-01-14**
- <https://github.com/torvalds/linux/commit/8429bb3975ef81c114cde4da111e64d224d19f83>

The commit is valuable because it records both the generic NAND-core hook and the Micron-specific representation used to drive it.

### Source B — Linux Hynix read-retry support, 2017

Upstream Linux commit:

- `626994e0748019f9987ac520f1dcfd0adb7e34c6`
- **`mtd: nand: hynix: Add read-retry support for 1x nm MLC NANDs`**
- repository timestamp: **2017-03-08**
- <https://github.com/torvalds/linux/commit/626994e0748019f9987ac520f1dcfd0adb7e34c6>

This commit is especially useful because the implementation has to obtain, validate, and apply a vendor-specific set of retry parameters rather than merely enumerate an abstract retry index.

### Companion-repository check

`tmzncty/computing-archaeology` was searched for `read retry` / NAND before this slice. No dedicated existing read-retry history was found to reuse. Broader NAND-interface and controller genealogy still belongs there if developed later; this file stays with the retention-specific control-state boundary.

---

## 3. Historical / implementation record — Micron, 2014

### 3.1 The generic ONFI transport does not make the retry policy generic

The Micron commit explicitly says that Micron exposes read-retry support through two vendor-specific pieces layered on ONFI mechanisms:

1. a **vendor-specific ONFI parameter block** indicates how many read-retry modes are available;
2. ONFI `GET_FEATURES` / `SET_FEATURES` are used with a **vendor-specific feature address** to read or switch the current retry mode.

The patch defines that Micron feature address as `0x89` (`89h`).

That distinction is important:

```text
standardized transport primitive
    !=
standardized read-retry representation
```

The existence of ONFI feature transport does not by itself specify Micron's retry-mode count or the meaning of feature address `89h`.

### 3.2 The retry mode is explicit transient control state

The commit records the recommended sequence as:

```text
PAGE_READ
    -> if ECC succeeds: done
    -> if ECC fails: SET_FEATURES 89h, mode 1
    -> PAGE_READ again
    -> if ECC still fails and another mode exists:
         increment mode and retry
    -> otherwise: true ECC error
    -> SET_FEATURES 89h, mode 0
       to return to the default state
```

The selected read-retry mode is therefore not merely a conceptual property of the medium. It is a **device control state deliberately changed by the reader** during recovery and then restored to the default mode.

This yields:

```text
retry capability
    !=
currently selected retry mode
```

and:

```text
successful read under retry mode N
    !=
physical threshold distribution rewritten
```

Returning the control register to mode `0` changes the interpretation/read condition, not the charge already stored in the NAND cells.

### 3.3 Capability metadata can differ even inside the same broad cell class

The commit says the patch was tested on **Micron MT29F32G08CBADA**, which supports **8 read-retry modes**. It also records a check of Micron vendor-table data against several device datasheets.

The table represented in the commit includes both MLC devices with retry support and at least one MLC device without it.

The safe result is therefore:

```text
MLC NAND
    !=
read-retry capability automatically present
```

A controller cannot infer the retry-mode count merely from the broad label `MLC`; device/family-specific capability information matters.

### 3.4 What this Micron implementation does not retain

The sequence in this patch returns the device to retry mode `0` after the attempt. The commit does not establish a durable per-page cache of which retry mode last succeeded.

Therefore:

```text
retry mode discovered useful for one read
    !=
proved persistent per-page recovery history
```

Later SSD firmware may retain richer histories, but this particular Linux implementation record does not prove that behavior.

---

## 4. Historical / implementation record — Hynix, 2017

### 4.1 The abstract operation is common; the parameter representation is not

The Hynix commit says all Hynix MLC NANDs produced with the 1x-nm process support read retry. It immediately adds a portability warning: the implementation may be reusable for other Hynix NANDs, but **the method used to obtain retry parameters can change**, and some NANDs use a **fixed set of values** rather than retrieving the values from a read-retry OTP area.

So even within one vendor family:

```text
same abstract function: read retry
    !=
same parameter-discovery mechanism
```

The driver defines Hynix-private command values and a structure containing:

- the number of private registers to set;
- register offsets;
- retry-mode values.

The code comment says the register set is NAND-specific, while the values may be predefined or extracted from an OTP area.

### 4.2 Recovery can depend on retained calibration metadata

For the 1x-nm MLC path, Linux reads a NAND-resident **read-retry OTP area** and derives the register values used for later retry modes.

This makes a useful retained-state distinction visible:

```text
user payload state
    !=
ECC redundancy
    !=
read-retry calibration / mode table
    !=
currently selected retry mode
```

The calibration table is not the user payload, yet it participates in whether the software can establish a useful read condition for that payload.

### 4.3 Nonvolatile calibration storage is not treated as infallible

The Hynix implementation contains an unusually revealing integrity measure. It defines a repeat count of **8** for the 1x-nm read-retry data and includes a `majority check` helper whose code comment says it is intended to overcome the unreliability of MLC NAND when reading the OTP area that stores read-retry parameters.

The implementation reads repeated candidate values and selects the majority value; it also handles inverse-form values in the layout.

The key retention result is not that the retry table is “fragile” in every device. It is narrower:

> The upstream implementation does **not** treat NAND-resident recovery calibration merely as an unquestionable constant. It validates redundant encodings before using them to configure the reader.

That supports:

```text
nonvolatile calibration state
    !=
infallible calibration state
```

and, at the system level:

```text
payload still physically recoverable in principle
    !=
this reader has necessarily recovered trustworthy retry parameters
```

The second relation is an engineering reconstruction, not wording from Hynix.

### 4.4 The Linux record preserves a vendor recommendation without proving its vendor-primary text

A `FIXME` in the Hynix patch says **Hynix recommends copying the read-retry OTP area into a normal page**. The implementation proceeds to initialize retry data from the OTP path.

This is useful evidence of what the Linux driver author understood the vendor recommendation to be, but no Hynix-primary application note or datasheet was independently recovered in this slice.

Therefore this file records only:

```text
Linux implementation record reports Hynix recommendation
    !=
independently verified Hynix-primary wording
```

The primary-vendor provenance remains an explicit evidence debt.

---

## 5. Engineering reconstruction — two different kinds of retry state

The Micron and Hynix implementations expose two distinct layers that are easy to collapse if read retry is described only as “try another voltage.”

### Layer A — durable or discoverable capability/calibration state

Examples in this slice:

- Micron vendor parameter data tells the software how many retry modes exist;
- Hynix may use fixed values or NAND-resident OTP calibration values;
- Hynix's OTP-derived path validates repeated values before constructing its runtime table.

### Layer B — transient selected read condition

Examples:

- Micron uses `SET_FEATURES 89h` to move among retry modes;
- Hynix writes NAND-private registers and applies the requested mode.

Thus:

```text
what retry settings are admissible / available
    !=
which retry setting is active now
```

A system can retain or reconstruct Layer A while still treating Layer B as ephemeral transaction state.

---

## 6. Cross-vendor result — a common software hook does not erase material heterogeneity

Linux can expose one generic `setup_read_retry`-style operation while Micron and Hynix reach that operation through different vendor-specific state:

```text
Linux generic retry call
    |
    +-- Micron
    |     vendor ONFI parameter block
    |     + vendor feature address 89h
    |     + retry-mode index
    |
    +-- Hynix 1x-nm MLC
          NAND-specific registers
          + private commands
          + fixed or OTP-derived parameter values
          + validation of repeated OTP data
```

Therefore:

```text
common API shape
    !=
common underlying calibration representation
```

and:

```text
functional interchangeability at one software boundary
    !=
identical historical mechanism underneath
```

This is precisely why the repository should not infer a universal NAND read-retry state machine from one vendor's interface.

---

## 7. Functional comparison — Case 149 OTP is a different authority problem

Case 149 studies Micron NAND OTP as a **payload/control-authority** mechanism in which data can be programmed and then subjected to an irreversible protection transition.

The Hynix path in this evidence uses an **OTP area as a carrier for read-retry calibration parameters**.

The shared word `OTP` does not make the cases equivalent:

```text
Case 149:
OTP area as intentionally exposed payload / protection state
    -> programming authority can be irreversibly retired

Case 85 Hynix deepening:
OTP area as reader-calibration source
    -> values are consumed to reconstruct a retry control table
    -> Linux validates redundant encodings before use
```

So:

```text
OTP-resident state
    !=
one universal OTP semantic role
```

and:

```text
one-time-programmed / factory calibration carrier
    !=
proof that every later read of that carrier is error-free
```

This is a **functional comparison**, not a claim that the Hynix retry OTP uses Micron Case-149 commands, protection semantics, page layout, or lifecycle.

---

## 8. Functional comparison — Case 36 refresh remains a separate maintenance act

Case 36 concerns read/correct/rewrite-style maintenance that renews a physical Flash embodiment.

This slice remains on the **read-path recovery** side:

```text
change retry mode / threshold condition
    -> re-read existing cells
    -> possibly recover an ECC-decodable payload
```

That is not yet:

```text
recover payload
    -> allocate / erase / program another embodiment
    -> retire or reclaim the old embodiment
```

Therefore:

```text
reader calibration recovered
    !=
payload physically refreshed
```

A read-retry success can restore present readability without restoring future retention margin.

---

## 9. Retained-state decomposition added by this slice

Case 85 can now distinguish at least the following states:

```text
physical NAND threshold distributions
    !=
ECC redundancy / current correction margin
    !=
retry capability metadata
    !=
retry calibration table or parameters
    !=
currently selected retry mode
    !=
optional higher-layer history of which condition worked before
    !=
rewritten / refreshed physical embodiment
```

The last-but-one item is intentionally marked **optional**: neither Linux commit proves that the generic raw-NAND stack persistently records successful per-page retry advice.

A reader can therefore fail for several different reasons that should not be collapsed:

- the cell state is outside all supported retry conditions;
- the ECC margin is exhausted;
- the software does not know the correct vendor retry procedure;
- the retry parameter/calibration state cannot be established reliably;
- a useful transient retry mode was not selected;
- a previously successful read was never followed by physical renewal.

---

## 10. Philosophical boundary — operational availability depends on an interpreter relation

The narrow conceptual result is:

> Retained charge is not the whole operational memory relation. Some NAND payloads are usable only through a reader that also knows how to establish the appropriate interpretation/calibration state.

That statement does **not** imply that calibration metadata is philosophically identical to the payload, that data are “immaterial,” or that every storage system requires the same kind of interpreter state.

The engineering evidence is enough to say only:

```text
physical trace survives
    !=
trace is necessarily recoverable through an arbitrary reader state
```

Read-retry parameter state is one concrete mechanism by which the apparatus participates in recoverability.

---

## 11. Explicit non-claims

This slice does **not** claim that:

1. Linux invented NAND read retry.
2. Micron invented read retry in 2014.
3. Hynix invented read retry in 2017.
4. the two merge dates are the first commercial availability dates of the underlying NAND features.
5. ONFI standardizes Micron feature address `89h`; the Linux patch explicitly calls it vendor-specific.
6. one generic Linux callback implies a standardized cross-vendor retry parameter format.
7. every MLC NAND requires read retry.
8. every Hynix NAND retrieves retry parameters from OTP; the commit explicitly warns that some use fixed values and other retrieval methods may differ.
9. Hynix retry OTP is the same interface or authority regime as Micron OTP in Case 149.
10. the Hynix OTP majority logic can recover arbitrary corruption.
11. the retry-parameter OTP is immune to media errors because it is nonvolatile.
12. a successful retry rewrites, refreshes, heals, or remaps the user data.
13. returning Micron mode `0` restores cell threshold distributions; it restores the default reader/control state.
14. Linux's raw-NAND implementation proves how a commercial SSD controller firmware performs read retry.
15. either commit proves persistent per-page caching of successful retry modes.
16. the Linux driver's comment about Hynix copying OTP parameters has been independently verified against a Hynix-primary document in this slice.
17. Micron and Hynix share a direct historical genealogy with the Toshiba patent family already used by Case 85 merely because all implement threshold-adjusted rereads.
18. failure to establish retry parameters means the payload has physically disappeared; it means only that this recovery apparatus may have lost a required relation.

---

## 12. Claim ledger

| Claim | Class | Evidence strength | Boundary |
|---|---|---:|---|
| Micron Linux support uses a vendor-specific ONFI parameter block for retry-mode count | historical implementation record | strong | upstream merged commit, not direct vendor datasheet inspection here |
| Micron uses vendor-specific feature address `89h` with ONFI feature commands | historical implementation record | strong | exact Linux implementation |
| Micron sequence restores mode `0` after retry attempts | historical implementation record | strong | says nothing about physical rewriting |
| MT29F32G08CBADA was tested with 8 retry modes | historical implementation record | strong | named device test in commit message |
| broad `MLC` label does not imply read-retry support for every enumerated Micron part | historical implementation record | moderate/strong | based on device table recorded in commit |
| Hynix retry parameters may be fixed or OTP-derived depending on NAND | historical implementation record | strong | explicit commit statement |
| Hynix 1x-nm implementation applies NAND-specific register values | historical implementation record | strong | source code |
| Linux validates repeated Hynix OTP-derived values using majority logic | historical implementation record | strong | source code + explanatory comment |
| recovery metadata can itself require integrity treatment | engineering reconstruction | strong | directly motivated by repeated/validated retry calibration |
| payload recoverability and recovery-parameter recoverability are distinct | engineering reconstruction | moderate/strong | system-level consequence, not vendor wording |
| Case 149 OTP and Case 85 retry OTP have different semantic roles | functional comparison | strong | grounded cases, no shared-interface claim |
| common software API does not imply common material/control representation | engineering reconstruction | strong | Micron/Hynix contrast |

---

## 13. Remaining evidence debt

This slice closes only the narrow roadmap debt around **vendor-specific read-retry parameter/control state in a deployed general raw-NAND stack**.

Still open:

- recover a **Micron-primary archived datasheet** for the exact devices and directly verify the vendor-specific ONFI table / byte-180 semantics used by the 2014 patch;
- recover a **Hynix-primary datasheet or engineering note** for the 1x-nm MLC retry-OTP format and the reported recommendation to copy the retry OTP area;
- reconstruct the exact Linux NAND-core retry-interface genealogy before and after these vendor drivers;
- trace when newer NAND interfaces moved from simple hard-decision retry modes toward richer soft-decision / LDPC assistance;
- obtain a named commercial SSD controller/firmware trace showing how retry calibration or successful-read history is retained internally;
- fault-inject corrupted retry-calibration metadata and distinguish inability to establish reader parameters from genuinely unrecoverable user data;
- move any broad vendor-command / raw-NAND interface history that emerges into `tmzncty/computing-archaeology` rather than duplicating it here.

---

## 14. Completion decision

This is a **bounded deepening**, not a new case and not a maturity promotion.

It closes one specific gap in Case 85:

> read retry is not only an alternate-threshold operation; in real raw-NAND support it can depend on vendor-specific capability and calibration state, and that recovery state may itself require validation before the payload can be interpreted successfully.

Case 85 should remain **`grounded`**. The direct vendor-primary calibration documents, commercial SSD firmware behavior, and soft-decision/LDPC genealogy remain open.