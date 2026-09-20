# Case 38 Deepening — SCT Feature-Control Persistence Is a Separate Retention Relation

## Purpose

This record deepens [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md) around one bounded question left deliberately open by the earlier Case 38 chronology work:

> when Intel's 2012 S3700 exposes `D000h (Power Safe Write Cache capacitor test interval)` through SCT Feature Control, what may be said about the lifetime of the selected interval across reset and power boundaries?

The answer is more precise than either of the easy extremes.

The earlier evidence correctly refused to infer persistence merely from the existence of `D000h`. The wider ATA/SCT command contract, however, already distinguishes **volatile** and **persistent** feature-state changes at the protocol layer. At the same time, the inspected Intel S3700 page does not publish the returned `D000h` option flags or an observed command trace proving which persistence option the shipping firmware accepts for that vendor feature.

The resulting bounded relation is:

```text
SCT Feature Control has a persistence selector
    !=
D000h is proven to support every selector on S3700
    !=
a particular host actually selected persistent state
    !=
that policy survived an observed reset / power cycle
```

**Evidence status:** `bounded deepening complete`.

---

## Related-repository check

Before writing, `tmzncty/computing-archaeology` was searched for `S3700`, `D000`, `SCT Feature Control`, and `Software Settings Preservation`. No dedicated indexed technical-history packet was exposed by the current search surface.

The broader history of ATA/SCT standardization belongs there if it is later developed as a protocol-history topic. This file keeps only the retention-specific control-state boundary needed by Case 38.

---

## Source set and custody

### A. Intel SSD DC S3700 Product Specification — 328171-001US

**Type:** Historical record / manufacturer-primary (`H/P`).

**Document:** Intel Corporation, _Intel Solid-State Drive DC S3700 Product Specification_, order 328171-001US, October 2012.

**Intel-hosted PDF:**

<https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

Directly inspected locations:

- cover: `ATA8-ACS2; includes SCT (Smart Command Transport)`;
- printed p. 24, §5.6: `Feature Control` plus feature codes `0001h`, `0002h`, `0003h`, and vendor feature `D000h (Power Safe Write Cache capacitor test interval)`;
- printed p. 25, §5.12: support for `Software Settings Preservation` through a SET FEATURES parameter;
- printed p. 26: standards reference to ACS-2 / ATA/ATAPI Command Set 2.

The Intel page directly establishes product support for an SCT Feature Control surface and the D000h feature name. It does **not** print the D000h state-value table or the option flags returned for D000h.

### B. INCITS T13 document index for ATA8-ACS

**Type:** Historical record / standards-organization metadata (`H/P`).

T13's current document-search index identifies the ATA8-ACS draft/finalization series, including D1699 revisions and D1699r6a, and dates the listed drafts. This is used to anchor the existence and chronology of the standard family rather than to substitute index metadata for command semantics.

T13 document search:

<https://t13.org/docsearch>

### C. ATA8-ACS / ACS-3 SCT Feature Control command text

**Type:** Historical record / standards text (`H/P`), with source-custody note below.

Publicly indexed copies of the T13 working-draft text preserve the SCT Feature Control layout:

```text
Action Code      0004h
Function Code    0001h Set state
                 0002h Return current state
                 0003h Return feature option flags
Feature Code     feature-dependent
State            feature-dependent
Option Flags     bit 0 = persistence selector
```

The working-draft language distinguishes two cases for a `Set state` operation:

- persistence bit set: requested feature-state change is preserved across the specified reset/power boundary;
- persistence bit clear: the requested state is volatile, and a hard reset causes reversion to the default or last nonvolatile setting.

The later ACS-3 draft wording is stronger and says the selected persistent feature state is preserved during **all power and reset events**.

The public T13 document index is authoritative for the draft series. The exact command-table text used here was cross-checked against publicly indexed working-draft copies and against smartmontools' source representation that explicitly cites `T13/1699-D Revision 3f, December 11, 2006, Table 72`. Because the current web gateway did not expose the historical T13 PDF bytes directly for page-image inspection, this record does **not** claim a fresh facsimile-level inspection of the original T13-hosted PDF.

### D. smartmontools source representation

**Type:** Engineering implementation witness / secondary standards transcription (`E/S`).

The current smartmontools ATA header defines `ata_sct_feature_control_command` with:

- action code `4`;
- function codes `1=set`, `2=return`, `3=return options`;
- `feature_code`;
- `state`;
- `option_flags`, with bit 0 described as persistent.

The source comment explicitly cites ATA8-ACS `T13/1699-D Revision 3f`, Table 72. This is useful corroboration of the command-wire representation, not a replacement for the standard and not product-specific proof about Intel D000h behavior.

### E. Later HGST / Western Digital OEM manuals

**Type:** Historical record / manufacturer-primary corroboration (`H/P`), later than the S3700 period.

Later SATA OEM manuals reproduce the same SCT Feature Control split: function `0003h` returns feature option flags, and option bit 0 distinguishes persistent from volatile state. These documents demonstrate that the persistence distinction remained an implemented vendor-facing command contract; they are **not** retroactive evidence that Intel D000h accepted a particular option on a 2012 S3700.

---

## Historical record

### H/P — Intel places D000h inside SCT Feature Control, not in a free-standing proprietary transport

The October-2012 S3700 specification says the device supports standard SCT actions and then lists `Feature Control`. Inside that action it names standard feature codes such as write cache and temperature-logging interval, and vendor feature `D000h (Power Safe Write Cache capacitor test interval)`.

This gives a safe product-level statement:

```text
D000h semantic meaning
    = Intel vendor feature: capacitor-test interval

transport/control envelope
    = SCT Feature Control
```

The first half is vendor-specific. The second half is a standardized command framework.

That distinction prevents two opposite mistakes:

- `D000h is vendor-specific, therefore the entire command has no standardized lifetime semantics`;
- `SCT Feature Control is standardized, therefore D000h's state values and every option are standardized`.

Neither follows.

### H/P — SCT Feature Control itself distinguishes current state from option capability

The command has different functions for:

```text
set feature state
return current feature state
return feature option flags
```

This is retention-significant. The current value and the **capability describing how that value may be retained** are not the same returned object.

A host that can read a current interval still has a separate question:

> does this feature advertise a persistence option, and how was the current setting installed?

### H/P — the protocol-level persistence selector distinguishes volatile and nonvolatile policy changes

The SCT Feature Control option word gives persistence a command-level representation. In the working-draft text, bit 0 controls whether a requested feature-state change is persistent or volatile. In the volatile case, hard reset returns the device to the default or the most recent nonvolatile setting.

That creates three different policy states:

```text
factory/default feature state
    !=
last nonvolatile feature state
    !=
current volatile override
```

This is closely analogous to the Current / Saved / Default distinctions seen in SCSI mode pages, but only as a controlled functional analogy. ATA SCT Feature Control and SCSI mode pages are different protocols and no genealogy is claimed here.

### H/P — Intel separately documents Software Settings Preservation

Immediately after the command-set sections, the same 2012 S3700 specification says the device supports a SET FEATURES parameter to enable or disable `Software Settings Preservation` (SSP).

ACS-family standards define SSP as a way to preserve certain software settings across SATA COMRESET rather than reverting them immediately. That mechanism is historically separate from the persistence bit carried by an SCT Feature Control `Set state` operation.

Therefore the Intel product exposes at least two distinct reset-lifetime concepts:

```text
SCT Feature Control persistence option
    !=
SATA Software Settings Preservation
```

The fact that both appear in one product manual is useful precisely because it warns against treating the word `preserve` as one universal state machine.

### H/P — Software Settings Preservation does not, by itself, prove D000h persistence

SSP is defined around preservation of particular software settings, especially settings established through SET FEATURES, across COMRESET. D000h is exposed through SCT Feature Control.

So this inference is rejected:

```text
S3700 supports SSP
therefore
D000h survives COMRESET / power cycle
```

The premises and conclusion concern different control paths.

### H/P — the S3700 manual does not publish D000h's returned option flags

The Intel specification names D000h, but the inspected section does not print:

- the D000h state encoding;
- its default interval;
- the result of Feature Control function `0003h` for D000h;
- whether a shipping S3700 accepts `Option Flags bit 0 = 1` for D000h;
- an induced-reset trace demonstrating restoration of a saved D000h value.

Accordingly this deepening closes a **protocol-semantics debt**, not the full **named-product persistence-observation debt**.

---

## Engineering reconstruction

### E — a maintenance policy has an embodiment and a lifetime

Case 38 already separates test cadence from last test result. The SCT persistence semantics add another axis:

```text
test cadence value
    !=
where / how that value is retained
    !=
how long the selected embodiment survives
```

A periodic self-test schedule can therefore be correct at time `t0`, become replaced by a volatile override, and later revert after reset without any change to the capacitor hardware itself.

### E — current policy and retained fallback policy can diverge

The standard's volatile/persistent distinction permits this generic reconstruction:

```text
nonvolatile policy = P_saved
current policy     = P_saved

host installs volatile override P_temp
current policy     = P_temp
nonvolatile policy = P_saved

hard reset
current policy     = P_saved
```

This is a protocol-level state model, not an observation that a particular S3700 firmware performed this exact sequence for D000h.

### E — policy persistence is separate from policy execution

Even if a capacitor-test interval is proven persistent, that only establishes retention of the **configuration relation**. It does not prove that every scheduled test actually executed.

```text
persistent cadence setting
    !=
test admitted
    !=
test executed
    !=
AFh updated
    !=
PLI readiness valid now
```

This connects cleanly to Synthesis 29's maintenance-observability distinction without turning Case 38 into a duplicate of that synthesis.

### E — persistence support, persistence selection, and persistence observation are different evidence levels

For any SCT feature, three questions should remain separate:

```text
1. protocol offers persistence semantics?
2. this feature/device reports that option as supported?
3. this actual setting was written persistently and survived the tested boundary?
```

The current evidence answers (1) at the standards layer and identifies the product/control relation needed for (2). It does not claim a laboratory answer to (3) for S3700 D000h.

### E — a control plane can retain the schedule for testing another retention mechanism

The conceptual stack is now more explicit:

```text
user payload durability obligation
    depends on
PLI emergency-transfer path
    whose future readiness is checked by
capacitor self-test
    whose cadence is governed by
D000h policy state
    whose own lifetime may be
volatile or persistent depending on control semantics
```

The layers are causally related but not identical. A failure at the outer control-policy layer may reduce future confidence without immediately corrupting NAND-resident payload.

---

## Controlled functional comparisons

### A — Case 14 SCSI AWRE/ARRE Current/Saved/Default state

Case 14's Seagate SCSI evidence distinguishes Current, Saved, and Default error-recovery policy. SCT Feature Control's volatile / nonvolatile / default relation is functionally comparable because both make **repair or maintenance policy itself** a retained object.

The comparison stops at function:

- SCSI MODE SELECT / mode pages and ATA SCT are different protocols;
- `Saved` in SCSI is not asserted to be the historical ancestor of SCT persistence flags;
- media-error reallocation policy is not PLI self-test cadence.

### A — Case 85 ONFI feature-state reset boundaries

Case 85 shows that reset behavior is state-class-specific rather than one universal rule. Case 38 now makes the same methodological point in an ATA/SCT setting:

```text
reset event
    + named state class
    -> specified survival / reversion relation
```

This is a functional comparison, not a shared mechanism or lineage claim.

### A — Synthesis 29 maintenance observability

Synthesis 29 separates configured cadence, admission, execution, coverage, accounting, and closure. The present case contributes a prior layer:

```text
configured cadence exists now
    !=
configured cadence will survive the next reset boundary
```

The synthesis remains cross-case; this file supplies one bounded protocol/control witness.

---

## Philosophical interpretation — bounded

The technical point can support one restrained interpretation:

> rules that govern remembering can themselves require remembering.

But the engineering content is exact and mundane: a controller exposes a maintenance interval, a command protocol distinguishes volatile from persistent feature-state changes, and reset may restore a prior nonvolatile value.

Nothing here implies human memory, institutional memory, intention, or self-awareness. `Second-order retention` is project language for a layered dependency, not historical ATA terminology.

---

## Explicit non-claims

This evidence does **not** claim that:

1. Intel invented SCT Feature Control.
2. Intel invented persistent device policy.
3. D000h is an ATA-standard feature code; Intel documents it as a vendor feature.
4. The state encoding of D000h is standardized by ATA.
5. The default D000h interval is established by the inspected 2012 page.
6. Every S3700 firmware revision accepts persistent D000h updates.
7. Function `0003h` is proven here to return bit 0 set for D000h on a physical S3700.
8. A host actually used persistent D000h on any deployment.
9. `supports Feature Control` means every feature supports every option.
10. A persistent Feature Control setting is the same thing as Software Settings Preservation.
11. SSP preserves every SCT vendor feature.
12. SSP survives a power cycle merely because it preserves selected state across COMRESET.
13. COMRESET, hard reset, software reset, and power-on reset are interchangeable terms.
14. A persistent cadence proves scheduled tests execute.
15. A scheduled test proves AFh was updated successfully.
16. AFh freshness proves whole-drive power-loss correctness.
17. Capacitor-test cadence is user payload.
18. Loss of D000h policy immediately destroys already NAND-resident data.
19. SCSI Saved mode pages and SCT persistence share a genealogy.
20. ONFI feature-state behavior and ATA feature-state behavior share a mechanism.
21. A standards-level persistence option proves product-level compliance.
22. smartmontools is treated as the normative ATA standard.
23. Later HGST/WD manuals are retroactive Intel S3700 evidence.
24. The current web copy of an ATA working draft is byte-identical to every historical T13-hosted revision.
25. This record replaces the need for a physical S3700 command/reset experiment.
26. Software Settings Preservation explains D000h.
27. `current value returned` proves `nonvolatile value returned`.
28. `feature option supported` proves `option selected`.
29. `option selected` proves `state survived` without observing the boundary.
30. Case 38 should be promoted beyond `grounded` on this evidence alone.

---

## Claim ledger

| Claim | Type | Evidence strength | Safe repository use |
|---|---|---:|---|
| S3700 exposes D000h capacitor-test interval through SCT Feature Control | H/P | Strong, Intel primary | Yes |
| S3700 separately supports Software Settings Preservation | H/P | Strong, Intel primary | Yes |
| SCT Feature Control separates set/current/options functions | H/P | Strong standards text + implementation corroboration | Yes |
| SCT Feature Control defines volatile vs persistent state-change semantics | H/P | Strong standards text + later vendor corroboration | Yes |
| Volatile state may revert to default / last nonvolatile state at hard reset | H/P | Strong standards text | Yes |
| SSP and SCT Feature Control persistence are distinct control relations | E | Strong reconstruction from separate standard mechanisms | Yes |
| S3700 D000h specifically advertises persistent option bit | H/P | Not directly inspected | No |
| S3700 D000h persistent setting survives real power cycle | X | Not experimentally observed | No |
| D000h persistent cadence guarantees self-test execution | E | False strengthening | No |

---

## Resulting bounded distinctions

```text
vendor feature semantic
    !=
standardized command envelope

current feature state
    !=
feature option capability

persistence capability
    !=
persistence selected for this update
    !=
persistence observed across a boundary

current volatile policy
    !=
last nonvolatile policy
    !=
default policy

SCT Feature Control persistence
    !=
Software Settings Preservation

persistent maintenance cadence
    !=
maintenance execution
    !=
maintenance evidence freshness
    !=
future power-loss survival
```

---

## Navigation / status update

- Canonical case remains [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md).
- Earlier chronology/control-surface deepening remains [`38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md`](38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md).
- Safe-degradation comparison remains [`38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md`](38-s3700-2013-ocp-2023-pli-failure-write-cache-authority-deepening.md).
- This file closes the **standards-level SCT persistence-semantics** portion of the D000h lifetime debt.
- Case 38 remains **`grounded`**. No maturity promotion is justified.

### Remaining narrow debt

The next useful evidence is no longer `does SCT have persistence semantics?`; that is now answered. The remaining named-product questions are narrower:

1. obtain an Intel D000h state/option table or equivalent manufacturer command reference if one survives;
2. issue Feature Control `Return feature option flags` for D000h on a physical S3700/S3500;
3. set distinct volatile and persistent D000h values and observe hard-reset / COMRESET / power-cycle behavior separately;
4. determine whether firmware update, secure erase, or sanitize-like service events preserve or reset the saved cadence;
5. observe whether AFh recency/test-count state itself survives the same boundaries independently of D000h policy.

Those would convert the present protocol-level reconstruction into named-firmware experimental evidence rather than merely making the prose more confident.

---

## Sources

### Manufacturer primary

Intel Corporation. _Intel Solid-State Drive DC S3700 Product Specification_, 328171-001US, October 2012.  
<https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

### Standards / institutional

INCITS Technical Committee T13. ATA8-ACS document series / document index.  
<https://t13.org/docsearch>

T13/1699-D, _AT Attachment 8 — ATA/ATAPI Command Set (ATA8-ACS)_, working-draft series. Publicly indexed historical copies; Feature Control command is cross-checked against the implementation citation below.

T13/2161-D, _ATA/ATAPI Command Set - 3 (ACS-3)_, working-draft series. Publicly indexed copy used to check the later persistence wording and Software Settings Preservation scope.

### Implementation / corroboration

smartmontools project. `atacmds.h` / ATA SCT Feature Control command structure, comments citing T13/1699-D Revision 3f Table 72.  
<https://github.com/mirror/smartmontools/blob/master/atacmds.h>

Western Digital / HGST SATA OEM product manuals, later SCT Feature Control sections, used only as later manufacturer corroboration of volatile/persistent option semantics.

---

## Final bounded conclusion

Case 38 can now say more than `D000h persistence is unknown`, but less than `D000h is proven persistent`.

The evidence supports this exact statement:

> **Intel's 2012 S3700 exposes the capacitor-test interval as vendor feature D000h inside SCT Feature Control. The SCT Feature Control protocol already has an explicit volatile-versus-persistent state-change model and a function for returning feature option flags. Intel's inspected S3700 page, however, does not publish D000h's returned option flags or a reset/power-cycle observation. Therefore the protocol provides a persistence mechanism for feature state, while D000h's shipping-product persistence support and actual selected lifetime remain separate empirical/product-documentation questions.**

That distinction matters to technical retention because the cadence used to qualify a future retention mechanism is itself state with a reset lifetime; neither the existence of the setting nor the existence of a persistence mechanism proves that a particular deployed policy will still be in force after the next boundary.