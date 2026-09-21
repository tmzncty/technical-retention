# Case 47 deepening — NVMe 2024 Post-Sanitize Media Verification and the verifier-visibility boundary

**Case:** 47 — FAST ’11 SSD sanitization verification  
**Status effect:** none; Case 47 remains `grounded`.  
**Slice:** NVM Express TP4152 / NVM Command Set Revision 1.1, UNH-IOL 2024 conformance procedures, and OCP Datacenter NVMe SSD Specification v2.6.  
**Question:** when a standardized SSD interface deliberately exposes sanitized media for verification, what exactly has become observable — and what has not?

---

## 1. Why this is a separate slice

Case 44 already establishes the older NVMe 1.3 relation:

```text
Sanitize command completion
    !=
Sanitize operation completion
```

Case 47 already establishes, from FAST ’11:

```text
reported erase success
    !=
independent lower-layer residual-state verification
```

This file does **not** repeat either result.

Instead it follows a later interface change. In 2024, NVM Express incorporated **TP4152, Post Sanitize Media Verification**, which adds a bounded state in which a host may read sanitized media for verification after sanitize processing has completed successfully.

That creates a new intermediate layer:

```text
sanitize processing succeeded
    -> Media Verification state
    -> controller-mediated media reads become available for verification
    -> host may evaluate returned data
    -> host exits verification
    -> Post-Verification Deallocation
    -> ordinary post-sanitize state
```

The central question is therefore no longer merely whether verification exists. It is:

> **what observation boundary does the new verification state expose?**

---

## 2. Source and chronology discipline

### 2.1 NVM Express Revision-2.1 change record

NVM Express's **Changes in NVM Express Specifications** document says it describes the specification set **as of August 2024** and identifies NVM Express Base Specification Revision 2.1 among that set.

Its TP4152 section describes **Post Sanitize Media Verification** as an optional feature. The same change record says TP4152 adds extensions to the Sanitize command, sanitize operations, and Read command to enable verification of correct sanitization by reading sanitized user data from media.

This is a historical standards record.

It is not evidence that every 2024 NVMe SSD implemented TP4152.

### 2.2 NVM Command Set Revision 1.1

The **NVM Express NVM Command Set Specification, Revision 1.1** is dated **August 5, 2024**. Its front matter explicitly lists TP4152 among the incorporated technical proposals.

Section 5.10.1 then gives the NVM-command-set-specific Media Verification read semantics.

### 2.3 UNH-IOL conformance plan

The University of New Hampshire InterOperability Laboratory **Test Plan for NVM Command Set Conformance, Version 22.0** is dated **August 15, 2024**.

This is an institutional conformance-test plan, not a published result for a named SSD. Its procedures are useful because they show what an external protocol-level tester can actually observe and assert.

### 2.4 OCP Datacenter NVMe SSD Specification v2.6

The Open Compute Project document identifies itself as **Datacenter NVMe SSD Specification, Version 2.6 (09252024)**. Its internal revision-history table separately lists the v2.6 update as **09/11/2024**.

This file preserves those two provenance signals rather than silently turning them into one exact publication date.

OCP v2.6 requires support for Sanitize Media Verification per TP4152.

---

## 3. Historical record — TP4152 creates a temporary verification state after successful sanitize processing

The NVM Command Set Revision 1.1 §5.10.1 states that while the sanitization target is in the **Media Verification state**, Read commands are processed under special rules and are not rejected merely with `Sanitize In Progress`.

The later Base Specification state-machine text describes the state more explicitly: sanitize processing has completed successfully, and media allocated for user data in the sanitization target is readable by the host for purposes of verifying sanitization.

This yields a historical interface distinction:

```text
sanitize processing completed successfully
    !=
verification opportunity already consumed
    !=
post-verification deallocation completed
```

The verification state is therefore not just a status bit attached to ordinary service. It is a distinct temporary operating state with a distinct observation contract.

---

## 4. Historical record — verification reads deliberately bypass ordinary integrity-failure behavior

NVM Command Set Revision 1.1 says that, when the command satisfies the Media Verification conditions and the controller can read the allocated media, the controller shall:

- ignore data-integrity errors for the purpose of returning that media data rather than automatically converting them into an ordinary unrecovered-read failure;
- return data read from the media;
- complete with the dedicated `Successful Media Verification Read` status when no other specified error applies.

Protection-information checking is not part of this path: a Read that requests PI checking is rejected with `Invalid Field in Command` under the bounded Revision-1.1 text.

The engineering significance is narrow but important:

```text
ordinary readable logical data
    !=
media data exposed for sanitize verification
```

TP4152 exists precisely because a successful erase mechanism may invalidate the ordinary integrity relation that would otherwise make normal reads fail before the host can inspect post-sanitize media content.

This is still a controller-mediated Read operation. It is not raw-chip acquisition.

---

## 5. Historical record — repeated verification reads need not be bitwise repeatable

Revision 1.1 explicitly allows the controller to return **different data on successive reads of the same LBA without intervening writes** while in Media Verification state. The example reason is to obscure media reliability characteristics.

The 2024 NVM Express change summary makes the rationale explicit at the feature level: the new read path exposes data after sanitization, but repeated reads may differ so that analysis of repeated reads does not reveal media characteristics.

This produces an unusual but well-bounded relation:

```text
host can inspect media-derived post-sanitize data
    !=
host receives a stable, repeatable raw-media image
```

A verification interface may increase observability while deliberately withholding another kind of observability.

That is not a contradiction. The contract is optimized for a sanitization check, not for unrestricted flash characterization.

---

## 6. Engineering reconstruction — `verification-readable` is its own state, not ordinary payload readability

The standards record supports the following project reconstruction:

```text
normal read contract
    -> current logical payload + ordinary integrity semantics

Media Verification read contract
    -> special post-sanitize media-derived observation
    -> integrity errors may be ignored for this purpose
    -> repeated returned values may differ
```

Therefore:

> **verification-readable != normally readable payload**.

The first relation exists so that applications can consume current data.

The second exists so that a host can gather evidence about a completed sanitization operation before the system returns to its later allocation/service state.

This distinction is engineering reconstruction. `verification-readable` is project shorthand, not NVM Express historical vocabulary.

---

## 7. Historical record — exiting verification changes the retained allocation relation again

The later NVMe sanitize state machine defines a **Post-Verification Deallocation** state. On exit from Media Verification, the controller proceeds to deallocate media allocated for user data in the sanitization target before returning to Idle, subject to the state-machine and failure rules.

UNH-IOL's 2024 test plan has an explicit Media Verification case that:

1. starts Block Erase or Crypto Erase with `EMVS=1`;
2. waits until sanitize progress reaches `FFFFh`;
3. issues `Exit Media Verification State`;
4. verifies transition through Post-Verification Deallocation and finally Idle.

This gives a second temporal distinction:

```text
sanitized medium temporarily retained in a verification-addressable relation
    !=
media retained in the ordinary allocation relation after verification
```

The verification window is therefore itself stateful and finite.

---

## 8. UNH-IOL 2024 — protocol conformance can test old-pattern mismatch without becoming raw-NAND forensics

UNH-IOL Version 22.0 includes a Media Verification procedure that writes a known pattern (`AA`) to ten blocks beginning at LBA 0, starts Block Erase or Crypto Erase with `EMVS=1`, waits for sanitize completion, and then reads those blocks while in Media Verification state.

Its observable result requires that the data patterns read during verification **do not match** the data patterns written before sanitization.

This is materially stronger than checking only:

```text
command returned success
```

because an external test host now observes data through the dedicated verification path.

But the procedure still does **not** establish:

```text
all hidden physical pages were independently enumerated
```

or:

```text
no analog remanence exists
```

or:

```text
controller firmware could not misrepresent underlying state
```

The bounded conformance statement is:

> the protocol exposes a testable post-sanitize data relation, and an external tester can compare that returned relation against a known pre-sanitize pattern.

That is a significant verification improvement while remaining an interface-level experiment.

---

## 9. OCP v2.6 — implementation support, conformance claim, and verification support are distinct fields

OCP v2.6 requires datacenter SSDs in its profile to support Sanitize and all three named operations in the relevant requirement: Block Erase, Overwrite, and Crypto Erase.

It separately requires **Sanitize Media Verification per TP4152** (`NVMe-AD-26`).

Its Device Capabilities log also defines a Sanitize-command-support field whose bit 15 is set when the device has been **tested and found to comply** with the Sanitize requirements of the OCP specification, while other bits separately indicate support for the Sanitize command and individual action classes.

That separation is useful:

```text
feature supported
    !=
feature profile requirements tested
    !=
media verification feature supported
```

However, the device-reported `tested and found to comply` bit is still a **device-reported claim about prior testing**. Reading that bit is not itself equivalent to possessing the underlying external test evidence.

Therefore:

```text
device says it was tested
    !=
independent verifier currently repeated the test
```

This is an engineering/evidence distinction, not a criticism of the OCP field.

---

## 10. OCP v2.6 also makes sanitization history persistent enough to be operationally visible

OCP v2.6 requires Persistent Event Log entries for:

- `Sanitize Start`;
- `Sanitize Completion`.

It also requires the device to ship with a defined initial relationship between Sanitize Status and Global Data Erased state, and requires retained asynchronous-event information when reporting is enabled but no request is currently outstanding.

The bounded retention relation is:

```text
sanitized payload should become unavailable
    while
sanitization-event / capability / state evidence remains observable
```

Again, retained evidence about forgetting is a different object from the user payload being forgotten.

This extends the Case-44 completion-state point but does not repeat it: the new contribution here is the later **verification-access and conformance-evidence surface** around that state.

---

## 11. Cross-case comparison — TP4152 versus FAST ’11 raw-NAND verification

### FAST ’11

FAST ’11 dismantles SSDs and reads flash through custom hardware. Its key strength is that the experiment bypasses the ordinary SSD controller interface and looks for surviving digital fingerprints in raw flash.

### TP4152 / NVMe 2024

TP4152 deliberately provides a controller-mediated verification state in the standard interface. It allows the host to inspect media-derived data that ordinary post-erase integrity handling might otherwise hide.

### Bounded comparison

```text
FAST '11 raw-flash path
    -> bypass controller's ordinary logical view
    -> independently inspect extracted flash contents

TP4152 Media Verification path
    -> remain inside controller/NVMe command path
    -> controller exposes media-derived data under special read semantics
```

Therefore:

> **standardized media-verification access != controller-bypassing raw-NAND acquisition**.

That does not make TP4152 weak or useless. It establishes a new, explicitly verifiable interface relation that did not exist in NVMe 1.3.

It simply means the two methods support different claims.

---

## 12. Cross-case comparison — NIST verification vocabulary and NVMe media verification are not synonyms

Case 47's NIST Rev. 1 deepening treats `verification` as operational evidence that a sanitization technique completed as intended, with technique- and media-dependent assurance considerations.

NVMe TP4152's `Media Verification state` is a particular protocol mechanism that exposes post-sanitize media-derived reads.

The relationship is:

```text
NIST-style sanitization verification
    = broader operational assurance category

NVMe Media Verification state
    = one storage-interface observation mechanism
```

Do not silently substitute one term for the other.

A policy may accept evidence without TP4152, and TP4152 availability by itself does not define a complete organizational sanitization-validation policy.

---

## 13. Verification visibility matrix

This slice closes one part of the previously open verifier-visibility debt.

| Observation layer | What can be observed in the bounded evidence | What is not established |
| --- | --- | --- |
| ordinary host LBA read | current logical value under ordinary command semantics | hidden stale embodiments |
| Sanitize Status / events | progress, state, completion/history signals | contents of every physical embodiment |
| TP4152 Media Verification read | media-derived post-sanitize data through a special controller-mediated Read path | controller-bypassing raw page/OOB image; stable repeated physical sample |
| UNH-IOL conformance procedure | known pre-pattern versus returned verification data; state transitions | named-product results unless a test report names the DUT; raw-NAND absence |
| OCP Device Capabilities | advertised support and a device-reported tested/compliant bit | underlying independent test record simply by reading the bit |
| FAST ’11 raw-flash acquisition | extracted digital flash remnants below ordinary drive interface | analog remanence after a correctly executed erase |

This matrix should not be read as a universal hierarchy from “weak” to “strong.” Each layer answers a different question.

---

## 14. Engineering reconstruction — evidence access can itself be a retained capability with a bounded lifetime

The standards support a narrow project-level model:

```text
sanitize transforms target state
    -> verification state temporarily preserves an observation path
    -> host gathers evidence
    -> exit retires that observation/allocation state
```

So a system may need to retain **access to evidence of a completed transformation** long enough for an observer to inspect it.

This differs from retaining the old payload as authoritative data. The old pattern is the thing being disproved; the verification relation is the thing intentionally kept available for a bounded interval.

A concise project formulation is:

> **evidence availability can have its own retention horizon.**

This phrase is repository interpretation, not NVM Express terminology.

---

## 15. Philosophical interpretation — evidence is not identical to the event it certifies

A narrow philosophical pressure survives the engineering record:

> an operation can be complete while the evidence by which another actor evaluates that operation remains a separate, temporary technical object.

For TP4152, the sanitization transformation and the host's opportunity to inspect media-derived results are distinct states.

The interface therefore makes a useful anti-collapse point:

```text
completed forgetting event
    !=
evidence channel for judging that event
```

No claim is made here about human memory, testimony, institutional trust in general, or epistemology as such.

---

## 16. Explicit non-claims

This deepening does **not** claim that:

1. TP4152 existed in NVMe 1.3;
2. every NVMe 2.1 device implements TP4152;
3. every OCP v2.6-marketed drive has been independently retested by this repository;
4. the OCP `tested and found to comply` bit is itself the underlying test report;
5. Media Verification Read is raw-NAND access;
6. Media Verification Read exposes page OOB/spare bytes;
7. Media Verification Read bypasses the SSD controller or FTL;
8. successive reads of one LBA must be bitwise identical in Media Verification state;
9. a differing post-sanitize pattern proves absence of every lower-layer digital copy;
10. a differing post-sanitize pattern proves absence of analog remanence;
11. a successful `Successful Media Verification Read` status proves the returned bytes are a unique physical-cell image;
12. ignore-integrity-error behavior means data-integrity protection is generally disabled outside Media Verification;
13. PI-enabled verification reads are permitted under the bounded Revision-1.1 rule;
14. UNH-IOL Version 22.0 reports a named device passing Case 27;
15. a conformance test plan is the same evidence class as a published device test result;
16. OCP v2.6 invented sanitization verification;
17. NVM Express TP4152 was caused by FAST ’11;
18. FAST ’11 and TP4152 use the same observation mechanism;
19. NIST `verification` and NVMe `Media Verification state` are synonymous historical terms;
20. the verification state is ordinary production-data service;
21. the post-verification deallocation state is itself evidence of physical block erase;
22. deallocation after verification proves every hidden physical embodiment has been erased;
23. a device capability bit is equivalent to independently witnessed implementation behavior;
24. controller-mediated verification is useless because it is not raw NAND;
25. raw-NAND analysis is required by NVMe TP4152;
26. raw-NAND analysis is required by OCP v2.6 merely because it requires TP4152;
27. the OCP header date and revision-history date are silently treated as one identical provenance event;
28. the Media Verification feature makes firmware trust irrelevant;
29. the new evidence promotes Case 47 to `mature`;
30. this bounded 2024 slice is a complete history of NVMe sanitization verification.

---

## 17. Remaining debt after this slice

This file partially closes Case 47's verifier-visibility mapping at the **standardized controller-interface / protocol-conformance** layer.

Still open:

- a named SSD + firmware test report that actually executes TP4152 Media Verification and publishes results;
- comparison of a TP4152 verification read with raw NAND/page/OOB acquisition on the same device;
- device behavior across firmware revisions;
- sanitize interruption / power-loss fault injection on a named device;
- controlled Cryptographic Erase followed by old-key / stale-key-bearing-metadata search;
- service-area/controller-metadata visibility that is neither ordinary LBA nor raw NAND;
- modern over-provisioning/remap residual-state experiments after standardized Sanitize;
- analog-remanence work remains a separate evidence class.

---

## 18. Related repository boundary

`tmzncty/computing-archaeology` was searched for `Post Sanitize Media Verification`; no dedicated packet was returned in this round.

A broad history of NVMe sanitization, OCP SSD qualification, controller architecture, and SSD test-tool evolution belongs there if developed later.

Case 47 keeps only the technical-retention relation:

```text
requested forgetting
    !=
implemented forgetting
    !=
verified forgetting
    !=
which layer the verifier was actually allowed to observe
```

---

## 19. Sources

### Primary standards

- NVM Express, **Changes in NVM Express Specifications**, as of August 2024, especially TP4152 Post Sanitize Media Verification: <https://nvmexpress.org/wp-content/uploads/NVM-Express-Revision-2.1-Changes-09_05_24.pdf>
- NVM Express, **NVM Express NVM Command Set Specification, Revision 1.1**, August 5, 2024, especially §5.10.1 Media Verification: <https://nvmexpress.org/wp-content/uploads/NVM-Express-NVM-Command-Set-Specification-Revision-1.1-2024.08.05-Ratified.pdf>
- Open Compute Project, **Datacenter NVMe SSD Specification, Version 2.6 (09252024)**, especially NVMe-AD-7, NVMe-AD-17 through NVMe-AD-26, STD-LOG-10, and DCLP-4: <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-6-2-pdf>

### Institutional conformance source

- University of New Hampshire InterOperability Laboratory, **Test Plan for NVM Command Set Conformance, Version 22.0**, last updated August 15, 2024, especially the Media Verification state/event cases and Test 1.17 Media Verification cases 11–29: <https://www.iol.unh.edu/sites/default/files/testsuites/nvme/v22/UNH-IOL_NVM_Command_Set_Conformance_v22.0_2024.08_15.pdf>

### Later continuity check

- NVM Express, **NVM Express Base Specification, Revision 2.2/2.3**, Media Verification State and Post-Verification Deallocation state. These later texts are used only to confirm continuity of the state-machine semantics, not to backdate later wording into the August-2024 document set.
