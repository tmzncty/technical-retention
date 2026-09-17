# Case 38 Deepening — Intel S3700 SCT Test-Cadence Persistence Boundary

## Status

**`bounded deepening complete`**

This evidence note deepens [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md) without changing its maturity.

The narrow question is:

> The Intel SSD DC S3700 exposes an SCT Feature Control code for the power-safe-write-cache capacitor-test interval. What does the period command contract let us say about the lifetime of that maintenance-policy state across reset and power boundaries?

The answer is narrower than “the S3700 definitely stores D000h in nonvolatile memory.” The October-2012 Intel product specification directly establishes that `D000h` is a vendor-specific **SCT Feature Control** item named `Power Safe Write Cache capacitor test interval`. A 17-October-2011 T13 ACS-3 working draft independently shows that SCT Feature Control was designed to separate:

- setting a feature state;
- reading its current state;
- reading its option flags; and
- choosing, through option flag bit 0, whether a requested state change is **preserved during all power and reset events** or remains **volatile**, in which case a hard reset returns to a default or the last nonvolatile setting.

That gives this case a stronger bounded relation than the canonical file previously had:

```text
maintenance-policy value
    !=
maintenance-policy persistence horizon

current feature state
    !=
last nonvolatile feature state
```

But the evidence still does **not** include an S3700 hardware transcript showing that firmware accepted the persistent option for `D000h`, nor a before/after power-cycle readback of the test interval. The source set therefore establishes a **protocol-level persistence choice surrounding the vendor feature**, not device-specific experimental proof of one chosen D000h persistence mode.

---

## 1. Source custody and chronology

### 1.1 Intel S3700 product specification — manufacturer-primary product contract

Intel Corporation, **_Intel Solid-State Drive DC S3700 Product Specification_**, order `328171-001US`, October 2012:

<https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

The inspected Intel-hosted PDF states that the S3700 supports ATA mandatory commands and includes a dedicated §5.6 `SMART Command Transport (SCT)` section. On printed p. 24, Intel says the drive supports standard SCT actions and, under `Feature Control`, lists:

- `0001h` — write cache;
- `0002h` — write cache reordering;
- `0003h` — temperature-logging interval;
- `D000h` — **Power Safe Write Cache capacitor test interval**;
- `D001h`–`D004h` — other vendor-specific power/governor controls.

The same product specification separately documents:

- the power-loss capacitor test (§2.9);
- SMART `AFh`, whose raw state includes the latest capacitor-discharge result, minutes since last test, and lifetime test count;
- §5.12 `Software Settings Preservation`, which says the device supports the SET FEATURES parameter for enabling/disabling preservation of software settings.

The latter is kept separate from the SCT Feature Control option-flag relation below. The inspected Intel passage does not say that D000h is implemented through the separate Software Settings Preservation feature set.

### 1.2 T13 ACS-3 working draft — period standards-development witness

T13/2161-D Revision 1b, **_ATA/ATAPI Command Set - 3 (ACS-3)_**, 17 October 2011, is a **working draft**, not a final published ANSI standard.

A surviving searchable copy was inspected for §8.3.4 `SCT Feature Control command`:

<https://www.scribd.com/document/1074396691/ATA8-ACS-3>

The official T13 document index independently records the ACS-3 draft series and later 2012 revisions:

<https://t13.org/docsearch?field_author_value=&field_document_number_value=&field_document_stage_target_id=All&field_document_type_target_id=All&field_document_type_target_id_1=All&order=field_document_number&page=11&sort=asc&title=>

This source is used for **period protocol semantics**, not as proof that Intel's October-2012 product was claiming compliance with this exact ACS-3 revision. Intel's own standards-reference table names ACS-2. The valid relation is therefore:

```text
period SCT Feature Control semantics
    +
Intel product use of SCT Feature Control for D000h

not

proof that Intel implemented every clause of ACS-3 Rev. 1b
```

### 1.3 Later implementation corroboration is not the historical anchor

Later open-source ATA tooling preserves the same conceptual split between a volatile feature setting and a persistent setting. That continuity is useful as an implementation cross-check, but this note does not use later tooling to back-project behavior into an S3700 firmware build.

The historical anchors remain the Intel 2012 product specification and the period T13 standards-development text.

---

## 2. Historical / interface record

### 2.1 Intel makes the capacitor-test interval a named control state

The October-2012 S3700 specification does more than state that a capacitor self-test exists. It exposes a distinct **test-interval** control through SCT Feature Control:

```text
D000h
    = Power Safe Write Cache capacitor test interval
```

This creates a fourth state category alongside the three AFh reporting fields already grounded in Case 38:

```text
last readiness-test result
    !=
time since last test
    !=
lifetime number of tests
    !=
policy controlling the test interval
```

The first three describe test evidence/history. D000h governs when future readiness evidence is to be refreshed.

### 2.2 SCT Feature Control separates “set”, “read current”, and “read options”

The 2011 ACS-3 working draft's SCT Feature Control command defines three relevant function codes:

```text
0001h  set state for a feature
0002h  return the current state of a feature
0003h  return feature option flags
```

That separation matters because it prevents a feature's present value from being treated as a complete description of its control contract.

A host may need to know at least:

1. what the feature is set to now;
2. what option behavior the feature supports; and
3. whether a requested change should remain volatile or be preserved.

### 2.3 Option flag bit 0 explicitly types the persistence horizon of a state change

For a `Set state` request, the same working draft defines option flag bit 0:

- bit 0 set to `1`: the requested feature-state change is to be preserved during **all power and reset events**;
- bit 0 cleared to `0`: the requested state change is **volatile**; a hard reset returns the device to the default value or to the last nonvolatile setting.

This gives a period standards-development vocabulary for a distinction that the repository otherwise might have introduced only analytically:

```text
current state
    !=
last nonvolatile state
```

and:

```text
set feature value
    !=
choose how long that value should remain authoritative
```

The command therefore carries both **content** and **persistence-policy** dimensions.

### 2.4 Vendor-specific feature code does not erase the generic control semantics

The ACS-3 table reserves `D000h`–`FFFFh` for vendor-specific Feature Codes. Intel uses `D000h` for its capacitor-test interval.

That combination is historically useful:

```text
generic SCT Feature Control envelope
    -> vendor-specific feature identity D000h
    -> vendor-specific state meaning
```

The generic envelope describes how feature state and option flags are transported. Intel supplies the product-specific meaning of D000h.

But the vendor-specific state encoding remains outside the inspected generic table. The T13 draft does not tell us what numeric interval values Intel accepts for D000h.

### 2.5 The product page does not publish D000h's option response

Intel's printed p. 24 establishes that D000h is supported under Feature Control, but it does not print:

- the allowed `State` values for D000h;
- the default capacitor-test interval;
- the value returned by `Return feature option flags` for D000h;
- whether every firmware revision accepts `Option Flags bit 0 = 1` for D000h;
- the actual nonvolatile medium or metadata structure used if a persistent D000h setting is accepted.

Therefore the strongest defensible historical claim is not:

> “S3700 D000h definitely survives power loss.”

It is:

> **Intel exposes the capacitor-test interval through a command family whose period protocol distinguishes current/volatile state from preserved/nonvolatile state, while the inspected product document does not itself disclose the D000h-specific option response or a power-cycle validation.**

---

## 3. Engineering reconstruction — maintenance policy is another retained state class

### 3.1 A readiness mechanism can depend on a policy about when to refresh evidence

Case 38 already separates the emergency PLI apparatus from evidence that the apparatus remains ready.

D000h adds one more layer:

```text
PLI apparatus
    -> periodic readiness test
    -> readiness result / recency / history

and separately

cadence policy
    -> decides when another readiness test should occur
```

The cadence value is neither user payload nor capacitor energy. It is control state about future maintenance-of-maintenance activity.

### 3.2 Current policy and saved policy can diverge

The SCT option semantics make this possible in principle:

```text
last nonvolatile test interval = A
current volatile test interval = B
```

If the volatile setting is then lost at a hard reset, the device may return to A (or to a default, depending on what saved/default state exists).

Thus:

```text
policy in force before reset
    !=
policy in force after reset
```

unless the relevant persistence condition has been established.

This is not a claim that an actual S3700 was observed in the `A/B` state. It is the engineering implication of the period SCT Feature Control state model.

### 3.3 Policy persistence does not prove policy execution

Even if a test interval survives every relevant reset boundary, several later relations remain open:

```text
cadence policy preserved
    !=
self-test became due
    !=
self-test actually executed
    !=
self-test completed
    !=
self-test passed
    !=
future real power-loss transfer succeeds
```

The policy controls when readiness evidence should be produced. It is not itself readiness evidence.

### 3.4 Readiness evidence persistence and cadence-policy persistence are different questions

AFh exposes result, recency, and lifetime-count state. D000h exposes cadence policy.

Those states can have different update rules and persistence horizons:

```text
last test result
    !=
when the next test is supposed to happen
```

No inspected source proves that AFh and D000h are stored atomically, updated in one transaction, or reconstructed from one common metadata record.

### 3.5 Maintenance policy is not maintenance progress

This slice should not be folded into Synthesis 26's restart-progress taxonomy without a type distinction.

A progress checkpoint asks:

> how far has the current maintenance job advanced?

D000h instead asks:

> on what cadence should a future readiness test be initiated?

Therefore:

```text
maintenance cadence policy
    !=
maintenance progress
    !=
maintenance result
```

A system may persist one of these and discard another without contradiction.

---

## 4. Reset / power-boundary matrix

| State / relation | Directly documented for S3700? | Period SCT relation | What remains unproved |
| --- | --- | --- | --- |
| capacitor self-test exists | yes | not needed | exact internal test implementation in every firmware |
| latest discharge-test result | yes, AFh | SMART reporting path | power-fail atomicity of AFh update |
| minutes since last test | yes, AFh | SMART reporting path | exact behavior through every reset/power-loss window |
| lifetime number of tests | yes, AFh | SMART reporting path | physical embodiment / update atomicity |
| capacitor-test interval control | yes, D000h | SCT Feature Control | allowed interval encoding/default |
| current feature state | D000h is named, value format not printed | Function `0002h` exists generically | actual readback transcript for D000h |
| feature option flags | not printed for D000h | Function `0003h` exists generically | actual D000h option response |
| volatile setting | not demonstrated for D000h | generic SCT option bit 0 = 0 relation | device-specific experiment |
| preserved setting | not demonstrated for D000h | generic SCT option bit 0 = 1 relation | device-specific experiment and storage embodiment |
| return after hard reset | not demonstrated for D000h | volatile setting returns to default / last nonvolatile setting | which D000h value an S3700 actually returns to |
| readiness test execution after reboot | no | outside generic persistence bit | scheduler/firmware behavior |
| whole-drive outage correctness | no | outside Feature Control | independent fault validation |

The matrix deliberately keeps **protocol capability**, **named product feature**, and **observed device behavior** as separate evidence classes.

---

## 5. Functional comparisons — not genealogy

### 5.1 Case 85 — NAND read-retry mode

Case 85's Micron witness shows an intentionally short-lived reader-configuration state: a selected read-retry mode persists across subsequent reads but is cleared at a documented power boundary.

Case 38 supplies a different relation: a control protocol can explicitly distinguish a volatile setting from a requested preserved setting.

The functional comparison is:

```text
control state can have a deliberately bounded horizon
    !=
all control state should be made persistent
```

No historical link from Micron read-retry design to Intel SCT cadence control is claimed.

### 5.2 Case 149 — transient mode versus durable authority

Case 149 separates a volatile NAND OTP operation-mode selector from an irreversible protection result.

Case 38 likewise warns against inferring the lifetime of one state from the lifetime of another state exposed by the same broader device.

The analogy stops there. OTP protection is an irreversible mutation-authority relation; D000h is a maintenance-scheduling control.

### 5.3 Synthesis 26 — restart progress policy

Synthesis 26 compares persistence policies for **maintenance progress** in HDFS, Kafka, and SQLite.

This S3700 slice adds a neighboring but distinct axis:

```text
progress horizon
    !=
policy horizon
    !=
evidence horizon
```

That is a candidate comparison dimension for later synthesis, not evidence that these systems share an implementation lineage.

---

## 6. Philosophical interpretation — policy about future evidence can itself require retention

The exact technical fact is modest:

> A device can expose a retained control value governing when it should next test the apparatus that protects data during future power failure, and the surrounding command protocol distinguishes volatile from preserved feature state.

A bounded interpretation is that technical retention can involve not only preserving payload or diagnostic evidence, but also preserving **rules for regenerating future evidence about retention capability**.

That supports a layered formulation:

```text
retain payload
    !=
retain protection capability
    !=
retain evidence about that capability
    !=
retain policy for refreshing that evidence
```

This is project interpretation, not Intel or T13 vocabulary. Intel does not say that the SSD is “remembering how to remember,” and that phrase should not be used as a historical claim.

The interpretation also has a hard limit: preserving the cadence rule is only useful if the rest of the scheduler, self-test mechanism, telemetry update path, and future PLI mechanism remain operational. A persistent policy is not a self-sufficient guarantee.

---

## 7. Explicit non-claims

This deepening does **not** claim that:

1. every Intel S3700 firmware accepts persistent option bit 0 for D000h;
2. D000h was experimentally observed to survive a power cycle;
3. D000h was experimentally observed to revert after a hard reset when set volatile;
4. Intel's D000h state encoding is defined by the generic T13 table;
5. the October-2012 Intel specification claims compliance with ACS-3 Revision 1b;
6. a 2011 ACS-3 working draft is identical to the final published ATA standard;
7. Intel's separate `Software Settings Preservation` subsection is the implementation mechanism behind SCT D000h persistence;
8. persistent option support implies a particular EEPROM, NAND page, reserved block, or controller NVRAM embodiment;
9. current feature state and last nonvolatile feature state are always different;
10. a persistent test interval proves that the self-test actually executes on schedule;
11. test execution proves test completion;
12. test completion proves a passing PLI result;
13. a passing capacitor self-test proves all future power-loss events are safe;
14. AFh result/history state and D000h cadence state are atomically updated;
15. AFh and D000h have the same persistence horizon;
16. the lifetime test count is a complete event log;
17. resetting a volatile cadence value loses the historical test count;
18. a maintenance-policy setting is the same thing as a maintenance-progress checkpoint;
19. later smartmontools behavior proves 2012 S3700 firmware behavior;
20. SCT Feature Control persistence semantics establish invention priority for persistent device configuration;
21. Case 85, Case 149, and Case 38 share a technical genealogy;
22. preserving a policy makes the system maintenance-free.

---

## 8. Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| October-2012 S3700 exposes D000h `Power Safe Write Cache capacitor test interval` under SCT Feature Control | H/P | strong: Intel 328171-001US, printed p. 24 |
| S3700 separately exposes AFh result, minutes-since-test, and lifetime-test count | H/P | strong: Intel 328171-001US, printed p. 19 |
| 2011 ACS-3 working draft has Set / Return current / Return option-flags functions for SCT Feature Control | H/P | strong standards-development witness; working draft |
| same working draft uses option flag bit 0 to distinguish preserved vs volatile requested feature-state changes | H/P | strong standards-development witness; working draft |
| volatile SCT Feature Control state can revert on hard reset to default or last nonvolatile setting | H/P | explicit in cited working draft |
| current feature state and last nonvolatile feature state are conceptually distinct in the period command model | E | strongly supported by explicit volatile fallback rule |
| test-cadence policy is distinct from self-test result/history | E | strongly supported by D000h vs AFh product surfaces |
| policy persistence, test execution, test success, and future outage success are separate relations | E | bounded reconstruction from distinct control/evidence layers |
| S3700 D000h specifically accepts persistent bit 0 and survives a real power cycle | X | not yet demonstrated |
| D000h uses the separate ATA Software Settings Preservation mechanism | X | not established |
| AFh and D000h updates are crash-atomic together | X | not established |
| a retained maintenance policy is the same as retained maintenance progress | X | explicitly rejected |

---

## 9. Remaining evidence debt

The next useful work is concrete rather than another conceptual rewrite.

### Device-specific command transcript

For a named S3700 firmware revision, collect:

1. `Return current state` for D000h;
2. `Return feature option flags` for D000h;
3. a volatile D000h setting;
4. readback before reset;
5. hard-reset / power-cycle boundary;
6. readback afterward;
7. a persistent D000h setting if the drive accepts it;
8. the same reset / power-cycle sequence.

That would close the gap between protocol semantics and observed product behavior.

### State encoding and default

Find manufacturer documentation, firmware tooling, or a controlled device experiment that establishes:

- D000h state units;
- legal range;
- factory/default cadence;
- behavior when persistence is unsupported or an option flag is invalid.

### AFh update boundary

The inspected product documents do not establish whether last-result, minutes-since-test, and lifetime-count fields are committed atomically under sudden power loss during or immediately after a capacitor self-test.

### Physical embodiment

No source inspected here identifies where a saved D000h value physically resides. The retention argument does not require guessing whether it is held in reserved NAND, another nonvolatile store, or reconstructed from some other metadata path.

### Historical lineage

A broader history of SCT Feature Control, Software Settings Preservation, vendor-specific enterprise-SSD management controls, and capacitor-PLI configuration belongs primarily in `tmzncty/computing-archaeology` if developed. This repository only needs enough genealogy to avoid presenting `current state != saved state` as an ahistorical invention.

---

## 10. Sources and inspection notes

### Primary manufacturer source

Intel Corporation, **_Intel Solid-State Drive DC S3700 Product Specification_**, order `328171-001US`, October 2012.

<https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

Directly inspected:

- printed p. 11 — power-off data retention and §2.9 capacitor-test surface;
- printed p. 19 — `AEh` unexpected-power-loss history and `AFh` result / recency / lifetime-count state;
- printed p. 24 — §5.6 SCT and D000h capacitor-test interval under Feature Control;
- printed p. 25 — standards references, including ACS-2;
- printed p. 25 / §5.12 vicinity — separate Software Settings Preservation statement.

### Period standards-development source

T13/2161-D Revision 1b, **_ATA/ATAPI Command Set - 3 (ACS-3)_**, 17 October 2011, §8.3.4 `SCT Feature Control command`, Tables 170–172. This is explicitly treated as a **working draft**.

Surviving searchable copy inspected:

<https://www.scribd.com/document/1074396691/ATA8-ACS-3>

Official T13 catalog used to verify the document series and later draft chronology:

<https://t13.org/docsearch?field_author_value=&field_document_number_value=&field_document_stage_target_id=All&field_document_type_target_id=All&field_document_type_target_id_1=All&order=field_document_number&page=11&sort=asc&title=>

The mirror supplies inspectable command text; the T13 catalog supplies authoritative document-series custody. Neither is silently upgraded into proof of the final published standard's wording.

---

## 11. Bounded result

The useful addition to Case 38 is not merely that “configuration can be persistent.” It is a more typed relation:

```text
retention infrastructure
    !=
readiness evidence
    !=
policy for refreshing readiness evidence

and

policy value
    !=
policy persistence horizon
```

Intel's 2012 S3700 documentation identifies the capacitor-test interval as SCT Feature Control state. Period SCT standards-development text independently makes the persistence horizon of a requested feature-state change explicit: the state may be volatile or requested as preserved across power/reset events.

The missing device-specific experiment remains important. Until an actual S3700 D000h option response and reset/power-cycle transcript is recovered, the repository should say **“protocol-level persistence choice around a named product control”**, not **“experimentally proven persistent S3700 test interval.”**