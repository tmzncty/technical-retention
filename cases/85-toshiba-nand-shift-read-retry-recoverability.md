# Toshiba NAND Shift Read / Retry Read: Mutable Read Thresholds, Recoverability Without Immediate Rewrite

**Status:** `grounded`

Grounding record: [`../evidence/85-flash-2000-2021-read-threshold-retry-grounding.md`](../evidence/85-flash-2000-2021-read-threshold-retry-grounding.md)

Vendor parameter-state deepening: [`../evidence/85-linux-2014-2017-vendor-read-retry-parameter-state-deepening.md`](../evidence/85-linux-2014-2017-vendor-read-retry-parameter-state-deepening.md)

Micron vendor mode-lifetime / power-boundary deepening: [`../evidence/85-micron-2015-read-retry-mode-power-boundary-deepening.md`](../evidence/85-micron-2015-read-retry-mode-power-boundary-deepening.md)

Micron reset-class / Hard Reset boundary deepening: [`../evidence/85-micron-2018-2020-read-retry-reset-class-boundary-deepening.md`](../evidence/85-micron-2018-2020-read-retry-reset-class-boundary-deepening.md)

## Scope

This case asks a narrow retention question:

> When the threshold-voltage distributions of NAND cells have drifted enough that a default read is not ECC-correctable, can the same physical cells still yield the intended logical data when the reader changes the decision thresholds, and what has — and has not — been retained when that succeeds?

The bounded historical center is Hiroyuki Nagashima's Toshiba memory-system patent family with Japanese priority **2009-11-06**, represented here by US20120268994A1 / US8929140B2 and later continuations. The family explicitly separates `default read`, `+ shift read`, `- shift read`, ECC determination, `retry read`, condition/history tables, and a later `refresh operation` that copies data to another erased block. A 2000-priority multi-level-Flash patent family is used only as an earlier prior-art witness for reference-voltage adjustment after ECC read failure. Park et al., ASPLOS 2021, provides a later independent empirical witness from **160 real 3D TLC NAND chips** that modern read-retry repeatedly senses a page with adjusted read-reference voltages until raw errors fall within ECC capability or the read is abandoned.

This is **not**:

- a general history of NAND sensing circuits;
- a claim that Toshiba invented adaptive reference-voltage reading or read retry;
- a history of every vendor's proprietary retry table;
- a replacement for Case 36's Correct-and-Refresh writeback regime;
- a replacement for Cases 52, 59, 65, and 67 on read disturb, program interference, early retention loss, and read-reclaim policy;
- a claim that any data which is physically present is necessarily recoverable;
- a claim that a successful shifted read has repaired or refreshed the medium;
- a full history of soft-decision LDPC, read-voltage tracking, or modern NAND calibration.

A broader command genealogy and vendor comparison belong primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Repository searches performed for these slices found no existing dedicated read-retry/reference-voltage or `89h` reset-semantics case there, so only the retention-specific mechanism is developed here.

---

## Historical vocabulary

The primary Toshiba family uses terms that should remain visible rather than being replaced by later abstractions:

- `read level`;
- `read voltage Vread`;
- `default read`;
- `+ shift read`;
- `- shift read`;
- `retry read`;
- `ECC` / `ECC error`;
- `program disturb (PD)`;
- `read disturb (RD)`;
- `data retention (DR)`;
- `standing time`;
- `management table`;
- `refresh operation`.

Park et al. use later vocabulary including:

- `read-retry`;
- threshold voltage `VTH`;
- read-reference voltage `VREF`;
- optimal reference voltage `VOPT`;
- raw bit-error rate `RBER`;
- `retry step`;
- `ECC-capability margin`.

The following are **project engineering-reconstruction terms**, not historical Toshiba or Park vocabulary:

- `read-decision state`;
- `interpretation margin`;
- `recoverability frontier`;
- `reader-side requalification`;
- `reset-class persistence horizon`.

They are useful only if their reconstructed status remains explicit.

---

## Retained state

At least five different state classes matter in the bounded mechanism.

### 1. Physical cell state

NAND cells retain charge / threshold-voltage distributions without continuous power. PD, RD, retention loss, cycling, and other mechanisms can move those distributions relative to the voltages used to classify them.

### 2. Read-decision parameters

The controller/device can use default or shifted read levels. In the Toshiba embodiment, read levels may be selected using use-state information and can be shifted upward or downward depending on the expected dominant error mechanism. Later read-retry literature describes repeated use of adjusted `VREF` values.

These parameters are not user payload. They are retained or reproducible **interpretation/control state** that affects whether the physical cell population can still be decoded.

### 3. ECC redundancy and decoding state

A page that produces too many raw errors at one set of reference voltages may be uncorrectable by the configured ECC, while a shifted read of the **same physical cells** can reduce the raw error count enough for ECC to recover the intended logical data.

Thus recoverability is not a property of raw media state alone.

### 4. Condition/history metadata

The Toshiba family explicitly discusses standing time, operation counts, temperature data, and management tables used to select read conditions. Later embodiments can retain a successful shift/index so future reads begin from a more appropriate boundary.

Again, this is not payload history. It is maintenance/interpretation state that helps future reads decide how to interrogate the payload.

### 5. Vendor capability and calibration state

Upstream Linux implementations from 2014 and 2017 expose another layer beneath the abstract act of “retrying a read.” Micron support obtains a retry-mode count from a vendor-specific ONFI parameter block and selects modes through vendor-specific feature address `89h`. Hynix 1x-nm MLC support can construct NAND-specific retry-register values from fixed parameters or an on-device retry-OTP area, validating repeated OTP values before use.

This adds two distinctions:

> **retry capability/calibration state != currently selected retry mode**

and

> **user payload state != metadata needed to establish a useful reader state**.

The 2015 Micron L83A family datasheet sharpens the persistence horizon of the second distinction: the device exposes eight retry options and makes feature `89h` the selected read condition for subsequent reads, but that selection lasts only until the feature is rewritten or the NAND is powered down. Thus `mode persists across commands != mode persists across power`.

A later Micron family with 2018 priority adds a second boundary: ordinary reset examples (`FFh`, `FCh`, `FAh`) may not reset feature `89h`, while `Hard Reset (FDh)` can return it to default; disclosed custom retry scratch state can live in internal SRAM and be cleared by `FDh` or power cycle. This does **not** retroactively establish the exact 2015 L83A `89h` behavior under `FFh`. It establishes that `reset` is too coarse a lifetime label unless the reset class and feature are named.

The detailed implementation record is kept in the linked vendor parameter-state, Micron mode-lifetime, and reset-class deepenings rather than generalized into a universal NAND format.

---

## Historical record

### H/P — default read and shifted read are distinct operations

US20120268994A1 describes an SSD using NAND flash and ECC. Its first embodiment states that threshold-voltage distributions can move upward under program/read disturbance and downward under data-retention loss. It responds by changing the read levels rather than immediately rewriting the cells.

The source explicitly describes:

- `default read`;
- a `+ shift read`, with read levels moved higher;
- a `- shift read`, with read levels moved lower;
- selection informed by conditions such as standing time and operation counts;
- temperature data as another possible input to the management table.

The important historical fact is therefore not merely that NAND had analog threshold distributions. The period source makes **the reading boundary itself an adjustable control variable**.

### H/P — first-read ECC failure can trigger retry read

The same patent family's second embodiment states that when the first read has a large error-bit count and ECC correction is impossible, a shift read — explicitly parenthesized as `retry read` — is performed and ECC correction is attempted again.

The mechanism can therefore be summarized historically without importing a modern metaphor:

1. read using one set of levels;
2. evaluate ECC correctability;
3. if uncorrectable, read again with shifted levels;
4. reevaluate ECC;
5. succeed or continue/fail according to the bounded retry policy.

Nothing in this sequence requires the payload cells to be rewritten before the second interpretation attempt.

### H/P — disturbance and retention can require shifts in opposite directions

The Toshiba family distinguishes upward threshold movement associated in its embodiment with PD/RD from downward movement associated with DR. Accordingly, it describes positive and negative read-level shifts rather than one universal retry direction.

This blocks a simplistic statement such as `old NAND always needs a higher read voltage`. The appropriate direction depends on the physical distribution change and the controller's model of it.

### H/P — successful reading and refresh remain separate

The patent also describes a `refresh operation` after reading when the error-bit count is large: data from the target block is copied to a new erased block. The text presents this as a distinct operation after read/ECC evaluation, not as an inherent part of shift read itself.

That separation is decisive for this case:

> **shift read can improve present recoverability without itself renewing the stored physical representation.**

The source even permits refresh to be omitted in some embodiments, which further prevents collapsing shifted sensing into rewrite-based maintenance.

### H/P — read conditions can themselves become retained management state

The patent family uses management tables and later continuations describe remembering successful read-condition indexes. This is a second-order retention mechanism: the system may preserve not only user data but also information about **how that data can currently be read successfully**.

This should not be overstated into a universal SSD implementation rule. It is directly established for the bounded patent family and is only functionally comparable to vendor retry-history schemes elsewhere.

### H/P — earlier reference-voltage recovery blocks a Toshiba-first claim

US20070201274A1 / US7333364B2, with claimed priority back to **2000-01-06**, describes MLC Flash in which read errors are detected with ECC and reference voltages can be adjusted to recover data. Its read-error flow changes references, rereads, checks the ECC error count, and can relocate data after recovery.

This is enough to reject the claim that the 2009-priority Toshiba family invented the general idea of adaptive reference-voltage rereading. It is **not** enough to establish a direct genealogy from the Super Talent family to Toshiba, nor to establish the first-ever use of the idea.

### S/E — modern 3D TLC confirms that the relation remains operationally important

Park et al., ASPLOS 2021, characterize **160 real 3D TLC NAND chips**. They describe modern read-retry as rereading a page with adjusted `VREF` values after ECC cannot correct the initial raw errors. The retry proceeds until the raw bit-error rate falls below the ECC correction capability or the page is determined unreadable.

Their experiments also show that retry behavior changes with operating condition, including retention age and P/E cycling. The final successful retry uses near-optimal reference voltages and can restore a positive ECC-capability margin.

This evidence is useful as a modern empirical witness, not as proof that every detail of Toshiba's 2009 embodiment was implemented identically in every later 3D NAND SSD.

### H/S — Linux 2014–2017 exposes vendor-specific retry state below the generic operation

A 2014 upstream Linux Micron implementation records read-retry capability through a vendor-specific ONFI parameter block and switches the active retry mode through ONFI feature commands at vendor-specific address `89h`; after the retry sequence it returns the device to mode `0`. A 2017 Hynix implementation exposes a different shape: NAND-specific register values may be fixed or obtained from a read-retry OTP area, and the OTP-derived path validates repeated values with majority logic before use.

This is historical **software-artifact** evidence rather than a claim that the two commits are first commercial implementations. Its retention-specific result is narrower:

> **a generic retry operation can depend on vendor-specific retained or discoverable calibration state, while the selected retry mode itself remains transient control state.**

The two implementations also block an easy standardization mistake:

> **common software hook != common vendor parameter representation**.

See the linked [`vendor read-retry parameter-state deepening`](../evidence/85-linux-2014-2017-vendor-read-retry-parameter-state-deepening.md) for exact commit provenance and non-claims.

### H/P — Micron 2015 makes the active-mode lifetime explicit

Micron's 2015 L83A 32Gb MLC family datasheet independently exposes the state shape reported by Linux. Its parameter page reports eight read-retry options, while configuration feature address `89h` selects `00h` as the default/disabled state and options `01h` through `07h` as alternate settings.

More importantly for retention, the vendor text says that after `89h` is written, subsequent array reads use the associated internal NAND settings until either the feature address is rewritten or the device is powered down. Once a retry becomes ECC-correctable, the flow directs the host to restore the retry option to default before the next array read.

This establishes a specific persistence horizon:

> **selected read-retry mode can persist across read commands without being a cross-power retained state.**

The datasheet is Rev. A **5/15**, so it is a later vendor-primary witness for the exact L83A/`MT29F32G08CBADA` family. It is not retroactively treated as proof of the exact wording in the datasheet consulted by the 2014 Linux patch author.

See [`85-micron-2015-read-retry-mode-power-boundary-deepening.md`](../evidence/85-micron-2015-read-retry-mode-power-boundary-deepening.md) for the source ledger, reset non-claims, and persistence-horizon comparison.

### H/P — Micron's 2018-priority family makes reset class part of read-retry lifetime

Micron's later `Read retry scratch space` family, priority **2018-01-12**, states in an example that reset commands such as `FFh`, `FCh`, and `FAh` may not reset feature address `89h` P1 data and disable Read Retry. The same disclosure says `Hard Reset (FDh)` can reset `89h` to its default value for a target LUN.

The family also discloses custom retry scratch state loaded into internal SRAM and says custom retry can be reset using `FDh` or a power cycle. This gives a later Micron-primary design witness for a state-lifetime distinction that the 2015 source could not close:

```text
ordinary reset example
    !=
hard-reset retirement boundary
    !=
power-cycle boundary
```

The patent wording is embodiment/design evidence, not a conformance report for every Micron product. It also does **not** prove that the 2015 L83A family preserves `89h` across `FFh`; that exact-family question remains open. See [`85-micron-2018-2020-read-retry-reset-class-boundary-deepening.md`](../evidence/85-micron-2018-2020-read-retry-reset-class-boundary-deepening.md).

---

## Engineering reconstruction

### E — physical threshold state ≠ read decision boundary

The physical distribution of cell threshold voltages and the voltage boundaries used to interpret that distribution are different state classes.

A cell population can remain physically unchanged between two successive attempts while the controller changes the boundary used to classify it.

### E — default-read failure ≠ physical data absence

If a default read produces an ECC-uncorrectable result, it follows only that the **current read path** has not recovered the codeword within its correction budget.

A later retry with different thresholds may recover the intended data from the same physical cells.

Therefore:

> `first-read uncorrectable ≠ no recoverable information remains in the cells`.

The converse is also important: physical presence of charge does not guarantee that any available sensing/ECC path can recover the intended logical value.

### E — retry read ≠ rewrite

Shift/read-retry changes how the stored analog state is sensed. It does not, by itself, create a fresh page image or reset the underlying threshold distribution.

This separates two kinds of retention work:

- **interpretive recovery** — change sensing parameters so ECC can recover the current logical value;
- **representation renewal** — rewrite/copy corrected data into a fresh physical embodiment.

The Toshiba source's later refresh/copy step makes this distinction historically defensible rather than purely philosophical.

### E — successful ECC recovery ≠ restored future margin

A retry can succeed because the adjusted thresholds move the raw error count back inside the ECC capability. That says the page is recoverable **now** under that read condition.

It does not imply:

- zero raw errors;
- a reset of cell wear;
- a restored threshold distribution;
- the same future retention margin as a fresh rewrite.

The Toshiba family's decision to refresh when the error count remains large is direct evidence that successful current correction and future-risk reduction are separable obligations.

### E — recoverability is relational

For this bounded case, logical recoverability depends jointly on at least:

1. the physical threshold-voltage distributions;
2. the chosen read/reference voltages;
3. the ECC code and correction capability;
4. controller policy for retry order and stopping;
5. optionally retained condition/history metadata used to choose a better starting point;
6. on implementations such as the 2014 Micron and 2017 Hynix Linux paths, vendor-specific capability/calibration state needed to establish valid retry settings.

No one component alone is `the retained data`.

This is the strongest conceptual contribution of the case. A state can remain recoverable even though a fixed/default interpretation has stopped working, because retention includes a **relation between substrate and reader**.

### E — read-condition metadata can preserve future interpretability

If a controller remembers a successful shift/index for a page, word line, or block, it is retaining evidence about the current interpretation boundary. That state can reduce future search work or make the next read more likely to start near a usable threshold.

But:

> `successful-read parameter ≠ complete physical-health model`.

The cell distribution continues to evolve, so a once-successful reference may become stale.

### E — retry calibration metadata can have its own integrity problem

The 2017 Hynix Linux path does not merely trust one OTP-derived retry value. It reconstructs values from repeated encodings and uses majority checking because the implementation explicitly anticipates unreliable reads of the MLC OTP area storing retry parameters.

This supports a narrower relation than “metadata is fragile”:

> **nonvolatile recovery metadata != automatically infallible recovery metadata**.

A payload may still carry recoverable physical structure while a particular reader has difficulty establishing the vendor-specific calibration relation needed to exploit it. That is an engineering reconstruction from the implementation, not Hynix's historical vocabulary.

### E — command-to-command persistence ≠ cross-power persistence ≠ generic reset semantics

The Micron 2015 vendor contract adds a smaller-grained state lifetime. A retry option selected through `89h` remains the reader condition for subsequent reads, but the stated lifetime ends when the feature is rewritten or the device is powered down.

Therefore:

> **runtime-retained reader configuration != power-retained reader configuration**.

A device can retain user payload across power while intentionally discarding the particular read-retry option that was active before power loss. Functional continuity is still possible because the supported retry state space can be rediscovered and a useful mode selected again.

The later Micron family shows why `reset` must remain a separate axis rather than being silently folded into power loss. In that design record, `FFh/FCh/FAh` may not reset feature `89h`, while `FDh` can. Thus:

```text
RESET command accepted
    !=
all runtime state retired
    !=
feature 89h defaulted
    !=
power removed
```

This **partially closes and reframes** the generic reset debt, but it still does not establish the exact L83A feature-`89h` behavior across every `RESET (FFh)` event.

### E — recoverability frontier can move without payload relocation

Project term: a `recoverability frontier` is the boundary between media states that the available sensing+ECC pipeline can still decode and states that it cannot.

This frontier can move in two ways:

- the cells drift relative to fixed read thresholds;
- the reader changes thresholds or decoding effort relative to fixed cells.

The term is deliberately reconstructive. Neither Toshiba nor Park is claimed to use it.

---

## Read, write, erase, and maintenance semantics

| Operation | Changes physical payload representation? | Changes read interpretation? | Can change current recoverability? | Renews media state? |
| --- | --- | --- | --- | --- |
| default read | not intentionally | uses default thresholds | yes, by observing current state | no |
| shift / retry read | not intentionally | **yes** | **yes** | no |
| ECC correction in controller | no NAND rewrite by itself | decodes observed bits | yes, at logical output | no |
| refresh/copy to erased block | **yes** | may use recovered data as source | yes | **yes, by creating a new representation** |
| erase/program cycle | **yes** | not merely interpretation | yes | creates another physical state, with wear cost |

The table is an engineering reconstruction of relations documented in the bounded sources; it is not a vendor command specification.

---

## Failure and forgetting

### Wrong boundary

A page may be physically recoverable but fail under a poorly chosen reference voltage because raw bit errors exceed ECC capability.

### Search exhaustion

If no available retry reference produces a codeword within the ECC budget, the controller reaches an uncorrectable end state for that read path. This is not evidence that every conceivable laboratory/forensic technique could recover nothing; it is the bounded system's operational failure boundary.

### Stale condition metadata

A formerly successful shift can become stale as retention age, cycling, temperature history, disturbance, or other cell characteristics change. Retaining a read condition therefore creates its own maintenance problem: **interpretation metadata can age even when it is not the user payload.**

### Invalid or unavailable retry calibration

Vendor-specific retry capability or calibration state can also become an operational dependency. The Hynix Linux implementation's repeated OTP values and majority validation are a concrete example of software treating recovery parameters as state that must itself be established credibly before use.

This failure mode should not be confused with proof that user payload charge has vanished.

### Reset-class mismatch

Software that treats every reset as equivalent can make the opposite mistake: it may assume feature `89h` has returned to default even though a bounded implementation permits the selected retry state to survive an ordinary reset. Conversely, assuming the state survives a stronger reset or power cycle can also be wrong.

The maintenance rule is therefore event-specific:

> **state lifetime must be attached to a named reset/power event, not to the word `reset` alone.**

### Recovery without renewal

A successful retry can conceal an approaching margin problem if the controller treats `correctable now` as `healthy indefinitely`. Toshiba's separate refresh decision and later empirical work on retry counts both prevent this collapse.

### Eventual rewrite / retirement

When read thresholds and ECC no longer provide adequate margin, systems may copy, refresh, reclaim, reduce density, or retire blocks. Those later actions are separate cases and should not be retroactively built into the definition of read retry.

---

## Cross-case comparison

### Case 36 — NAND Correct-and-Refresh

[`36-nand-flash-correct-and-refresh-maintenance.md`](36-nand-flash-correct-and-refresh-maintenance.md) studies a retention-maintenance path in which corrected data is rewritten/refreshed before errors become uncorrectable.

Case 85 supplies the complementary boundary:

> **reader-side recovery can occur before representation renewal.**

`retry-read success ≠ Correct-and-Refresh completion`.

### Case 52 — read disturb

[`52-nand-flash-read-disturb-access-induced-decay.md`](52-nand-flash-read-disturb-access-induced-decay.md) establishes that reading can itself contribute to physical threshold drift in neighboring cells. Case 85 does not repeat that physics. It asks how a controller can change interpretation when drift has already moved distributions relative to default sensing thresholds.

`disturb mechanism ≠ retry mechanism`.

### Case 59 — program interference

[`59-nand-program-interference-write-induced-neighbor-drift.md`](59-nand-program-interference-write-induced-neighbor-drift.md) studies write-induced neighbor drift. The Toshiba family explicitly includes PD among conditions motivating shift direction, but Case 85 treats PD only as an input condition to adaptive sensing.

`source of drift ≠ read-side compensation`.

### Case 65 — early retention loss / age-aware reading

[`65-3d-nand-early-retention-loss-age-aware-reading.md`](65-3d-nand-early-retention-loss-age-aware-reading.md) already shows that retention age can inform reading policy in 3D NAND. Case 85 deepens the narrower decision-boundary question with a period patent chain and explicit retry/ECC loop.

The cases are adjacent, not duplicates: Case 65 is primarily about asymmetric early retention loss and age-aware recovery; Case 85 is about **default-read failure followed by changed read thresholds without immediate rewrite**.

### Case 67 — read-disturb adaptive reclaim

[`67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md) turns observed read-disturb pressure into reclaim/relocation policy. Case 85 can stop earlier: it can recover a logical page by changing sensing conditions while leaving location unchanged.

`read-side requalification ≠ reclaim/relocation`.

### Case 82 — COPYBACK

[`82-micron-nand-copyback-ecc-requalification.md`](82-micron-nand-copyback-ecc-requalification.md) supplies almost the mirror image:

- COPYBACK can change physical embodiment without automatically requalifying integrity;
- read retry can change **interpretation** without changing physical embodiment.

Together they require at least three independent axes:

> `location continuity`, `interpretation continuity`, and `integrity-margin continuity`.

### Case 149 — NAND OTP authority vs retry calibration

[`149-micron-nand-otp-data-protect-irreversible-authority.md`](149-micron-nand-otp-data-protect-irreversible-authority.md) studies an OTP area as intentionally programmed payload/control state whose future programming authority can be irreversibly retired. The 2017 Hynix implementation used here instead consumes an OTP area as a source of read-retry calibration parameters and validates redundant values before applying them.

The comparison is functional only:

> **OTP-resident state != one universal OTP semantic role.**

The newer reset-class evidence adds a second bounded comparison: volatile/reset-bounded interpretation or access modes can coexist with nonvolatile substrate state. No shared command set, protection semantics, or direct vendor genealogy is inferred.

### Case 38 — current versus saved feature state

[`38-intel-s3700-power-loss-imminent-capacitor-self-test.md`](38-intel-s3700-power-loss-imminent-capacitor-self-test.md) distinguishes current feature state from saved/nonvolatile feature state and keeps reset/power behavior feature-specific. Case 85 now supplies a raw-NAND counterpart: capability, currently selected read-retry state, ordinary-reset survival, hard-reset survival, and cross-power survival are separate questions. This is a functional persistence-horizon comparison only.

### Case 76 — JEDEC SSD endurance / retention qualification

[`76-jedec-ssd-endurance-retention-qualification.md`](76-jedec-ssd-endurance-retention-qualification.md) concerns a qualification contract at rated endurance and power-off retention conditions. Case 85 concerns a runtime mechanism for making a particular page readable. A read-retry success does not change the drive-level JESD218 qualification meaning, and a JESD218 retention requirement does not specify one universal retry implementation.

---

## Functional analogies

The following are **functional only**:

- adjusting a radio receiver's tuning to recover a still-present signal;
- changing an analog comparator threshold to classify a noisy state;
- changing an OCR threshold/model while leaving the scanned page unchanged;
- a receiver whose ordinary reset aborts work while a stronger reset restores a tuning preset to default.

These analogies make the role of interpretation and event-specific state lifetime visible, but they establish no historical genealogy and should never substitute for NAND evidence.

---

## Philosophical interpretation — bounded

This case supports one limited philosophical proposition:

> A retained technical state need not be available under one timeless interpretation rule. Availability can depend on a maintained relation between a changing substrate and a changing reader.

That does **not** mean that data is immaterial, or that interpretation can rescue any degraded substrate. The physical threshold distributions, sensing electronics, ECC redundancy, and controller policy jointly delimit what can still be recovered.

The newer reset-class evidence adds a second restrained proposition: `reset` is not a metaphysical return to an original state. It is a technically specified retirement of some state relations while others may survive. Continuity and discontinuity are therefore **state-class × event-class relations**, not properties of a device taken as an undifferentiated whole.

The useful contrast is therefore not `matter versus meaning`, but:

- physical state that still carries discriminable structure;
- an interpretation boundary that may no longer fit it;
- technical work that changes the boundary;
- a specified event that may retire one interpretation state without erasing the substrate;
- a later decision about whether the representation itself must be renewed.

A successful retry demonstrates retained operational recoverability under a new read condition. It does not prove metaphysical identity, pristine media, archival permanence, or unlimited reversibility.

---

## Prior-art boundary

Safe claims:

- by a **2000-priority** MLC-Flash patent family, ECC-triggered reference-voltage adjustment and rereading were already explicit engineering proposals;
- by Toshiba's **2009-priority** family, an SSD/NAND design explicitly separated default read, positive/negative shift read, retry read, ECC evaluation, condition/history tables, and a distinct refresh/copy operation;
- by **2014**, upstream Linux Micron support exposed a vendor-specific retry-mode count and vendor-specific feature address `89h` behind a generic NAND retry interface;
- by **2015**, a Micron-authored datasheet for the L83A 32Gb MLC family including `MT29F32G08CBADA` exposed eight read-retry options, feature address `89h`, and an explicit selected-mode lifetime ending on feature rewrite or power-down;
- by **2017**, upstream Linux Hynix support exposed NAND-specific retry registers and fixed-or-OTP-derived calibration values, including validation of repeated OTP data;
- in a Micron family with priority **2018-01-12**, ordinary reset examples (`FFh/FCh/FAh`) were explicitly distinguished from `Hard Reset (FDh)` with respect to feature-`89h` retirement, and custom retry scratch state was disclosed in internal SRAM with FDh/power-cycle reset semantics;
- by **2021**, independent characterization of 160 real 3D TLC NAND chips showed modern read-retry repeatedly adjusting read-reference voltages and relying on the relation between RBER and ECC capability.

Unsafe claims rejected here:

- Toshiba invented read retry;
- the 2000 patent is the first adaptive sensing proposal of any kind;
- the 2000 patent directly caused the Toshiba design;
- Linux's 2014/2017 merge dates are the first commercial dates for Micron/Hynix read retry;
- the 2015 Micron revision proves the exact vendor wording available to the Linux author before the 2014 merge;
- the 2018-priority Micron patent proves every disclosed reset behavior shipped in a commercial product;
- the later Micron family proves exact 2015 L83A feature-`89h` behavior across `FFh`;
- all reset commands clear all NAND feature state;
- ONFI standardizes one cross-vendor retry parameter format or Micron feature address `89h`;
- every commercial SSD stores per-page successful retry voltages in the same way;
- all modern NAND uses the same retry direction/table/step count;
- retry read is equivalent to refresh, reclaim, COPYBACK, or secure rewrite.

A complete genealogy of adaptive sensing, reference cells, soft-decision decoding, proprietary retry commands, reset-command classes, LDPC, and vendor-specific calibration belongs in `computing-archaeology` if pursued.

---

## Sources

Primary / contemporary:

- Hiroyuki Nagashima, **“Memory system,”** US20120268994A1 / US8929140B2, Japanese priority 2009-11-06, Toshiba assignment record: <https://patents.google.com/patent/US20120268994A1/en>.
- Hiroyuki Nagashima, later continuation **US9524786B2**, “Memory system changing a memory cell read voltage upon detecting a memory cell read error”: <https://patents.google.com/patent/US9524786B2/en>.
- Frank Yu et al., **“Cell-Downgrading and Reference-Voltage Adjustment for a Multi-Bit-Cell Flash Memory,”** US20070201274A1 / US7333364B2, claimed priority 2000-01-06: <https://patents.google.com/patent/US20070201274A1/en>.
- Linux upstream commit `8429bb3975ef81c114cde4da111e64d224d19f83`, **“mtd: nand: support Micron READ RETRY,”** 2014-01-14: <https://github.com/torvalds/linux/commit/8429bb3975ef81c114cde4da111e64d224d19f83>.
- Micron Technology, **“32Gb, Asynchronous/Synchronous NAND,”** `L83A_32Gb_Async_Sync_NAND_mlc_plus.pdf`, Rev. A 5/15 EN, PDF ID `09005aef8644c380`; Micron-authored document recovered from a public mirror: <https://www.unikeyic.com/media/datasheet/d9/6b/ded2/d9/8c2c3bd5996175045d2af62c6e827efe.pdf>.
- Linux upstream commit `626994e0748019f9987ac520f1dcfd0adb7e34c6`, **“mtd: nand: hynix: Add read-retry support for 1x nm MLC NANDs,”** 2017-03-08: <https://github.com/torvalds/linux/commit/626994e0748019f9987ac520f1dcfd0adb7e34c6>.
- Rahul Mitchell Jairaj, Mark A. Hawes, Terry M. Grunzke / Micron Technology, **“Read retry scratch space,”** priority 2018-01-12, US20200371876A1 / US11586498B2: <https://patents.google.com/patent/US11586498B2/en>.

Independent later empirical witness:

- Jisung Park, Myungsuk Kim, Myoungjun Chun, Lois Orosa, Jihong Kim, Onur Mutlu, **“Reducing Solid-State Drive Read Latency by Optimizing Read-Retry,”** ASPLOS 2021, DOI 10.1145/3445814.3446719; open manuscript: <https://arxiv.org/abs/2104.09611>.

Related repository cases:

- [`36-nand-flash-correct-and-refresh-maintenance.md`](36-nand-flash-correct-and-refresh-maintenance.md)
- [`38-intel-s3700-power-loss-imminent-capacitor-self-test.md`](38-intel-s3700-power-loss-imminent-capacitor-self-test.md)
- [`52-nand-flash-read-disturb-access-induced-decay.md`](52-nand-flash-read-disturb-access-induced-decay.md)
- [`59-nand-program-interference-write-induced-neighbor-drift.md`](59-nand-program-interference-write-induced-neighbor-drift.md)
- [`65-3d-nand-early-retention-loss-age-aware-reading.md`](65-3d-nand-early-retention-loss-age-aware-reading.md)
- [`67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md)
- [`76-jedec-ssd-endurance-retention-qualification.md`](76-jedec-ssd-endurance-retention-qualification.md)
- [`82-micron-nand-copyback-ecc-requalification.md`](82-micron-nand-copyback-ecc-requalification.md)
- [`149-micron-nand-otp-data-protect-irreversible-authority.md`](149-micron-nand-otp-data-protect-irreversible-authority.md)

---

## Case conclusion

Case 85 adds a retention regime that is easy to miss if storage is treated only as `bits on media`:

> **the same physical NAND cells can move from default-read failure back into logical recoverability because the system changes how it reads them, not because it has already rewritten them.**

The retained object is therefore not adequately described by media survival alone. Operational availability depends on a relation among physical threshold distributions, adjustable read boundaries, ECC capability, controller policy, and — in some implementations — vendor-specific capability/calibration state needed to establish a useful read condition. The Micron family witnesses add that even inside this relation, the supported retry state space, the currently selected retry state, and the event that retires that state can have different lifetimes: a mode can persist across commands, later Micron examples distinguish ordinary resets from Hard Reset, and power remains a separate boundary. When the relation becomes unfavorable, interpretation work can temporarily restore access; when the physical representation itself must be renewed, refresh/copy is a separate maintenance act.

That distinction — `recoverability renewal ≠ representation renewal`, with `reset class ≠ one universal state-lifetime boundary` — remains the bounded contribution of this case.